import argparse
import sys
from typing import List
from tabulate import tabulate
from redis_manager import get_redis_manager
import json


class ValidationCLI:
    """CLI tools for vocabulary validation"""
    
    def __init__(self):
        self.redis_manager = get_redis_manager()
    
    def list_pending(self, word_type: str = None):
        """List all pending words"""
        words = self.redis_manager.get_all_pending_words()
        
        if word_type:
            words = [w for w in words if w['word_type'] == word_type]
        
        if not words:
            print("ℹ️  No pending words found")
            return
        
        # Prepare table data
        table_data = []
        for word in words:
            table_data.append([
                word['word'],
                word['word_type'],
                word['usage_count'],
                word['submitted_at'][:10],  # Date only
                word.get('notes', '-')[:50]  # Truncate notes
            ])
        
        headers = ['Word', 'Type', 'Usage', 'Submitted', 'Notes']
        print(f"\n📋 Pending Words ({len(words)} total)\n")
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        print()
    
    def show_details(self, word: str):
        """Show detailed information about a word"""
        word_data = self.redis_manager.get_pending_word(word)
        
        if not word_data:
            print(f"❌ Word '{word}' not found in pending list")
            return
        
        print("\n" + "="*60)
        print(f"📝 Word Details: {word_data['word']}")
        print("="*60)
        print(f"Type:          {word_data['word_type']}")
        print(f"Usage Count:   {word_data['usage_count']}x")
        print(f"Submitted:     {word_data['submitted_at']}")
        print(f"Submitted by:  {word_data['submitted_by']}")
        print(f"Status:        {word_data['status']}")
        print(f"\nNotes:\n{word_data.get('notes', '-')}")
        print("="*60 + "\n")
    
    def approve_word(self, word: str):
        """Approve a word"""
        word_data = self.redis_manager.get_pending_word(word)
        
        if not word_data:
            print(f"❌ Word '{word}' not found")
            return False
        
        # Confirm approval
        print(f"\n🔍 Word to approve: {word}")
        print(f"   Type: {word_data['word_type']}")
        print(f"   Notes: {word_data.get('notes', '-')}")
        
        confirm = input("\n✅ Approve this word? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Approval cancelled")
            return False
        
        # Approve in Redis
        success = self.redis_manager.approve_word(word)
        
        if success:
            print(f"✅ Word '{word}' approved successfully")
            print("   Will be added to cfg_grammar.py in next sync")
            return True
        else:
            print(f"❌ Failed to approve word '{word}'")
            return False
    
    def reject_word(self, word: str, reason: str = ""):
        """Reject a word"""
        word_data = self.redis_manager.get_pending_word(word)
        
        if not word_data:
            print(f"❌ Word '{word}' not found")
            return False
        
        # Show word info
        print(f"\n🔍 Word to reject: {word}")
        print(f"   Type: {word_data['word_type']}")
        print(f"   Notes: {word_data.get('notes', '-')}")
        
        # Get rejection reason if not provided
        if not reason:
            reason = input("\n📝 Rejection reason: ")
        
        # Confirm rejection
        confirm = input("\n❌ Reject this word? (y/n): ")
        if confirm.lower() != 'y':
            print("✅ Rejection cancelled")
            return False
        
        # Reject in Redis
        success = self.redis_manager.reject_word(word, reason)
        
        if success:
            print(f"❌ Word '{word}' rejected successfully")
            print(f"   Reason: {reason}")
            return True
        else:
            print(f"❌ Failed to reject word '{word}'")
            return False
    
    def batch_approve(self, words: List[str]):
        """Approve multiple words at once"""
        print(f"\n📦 Batch approving {len(words)} words...\n")
        
        approved = []
        failed = []
        
        for word in words:
            if self.redis_manager.approve_word(word):
                approved.append(word)
                print(f"✅ {word}")
            else:
                failed.append(word)
                print(f"❌ {word}")
        
        print(f"\n📊 Results:")
        print(f"   Approved: {len(approved)}")
        print(f"   Failed: {len(failed)}")
        
        if failed:
            print(f"\n⚠️  Failed words: {', '.join(failed)}")
    
    def batch_reject(self, words: List[str], reason: str):
        """Reject multiple words at once"""
        print(f"\n📦 Batch rejecting {len(words)} words...\n")
        
        rejected = []
        failed = []
        
        for word in words:
            if self.redis_manager.reject_word(word, reason):
                rejected.append(word)
                print(f"❌ {word}")
            else:
                failed.append(word)
                print(f"⚠️  {word}")
        
        print(f"\n📊 Results:")
        print(f"   Rejected: {len(rejected)}")
        print(f"   Failed: {len(failed)}")
    
    def sync_to_cfg(self):
        """Sync approved words to cfg_grammar.py"""
        from cfg_updater import CFGUpdater
        
        print("\n🔄 Syncing approved words to cfg_grammar.py...\n")
        
        updater = CFGUpdater()
        result = updater.sync_approved_words()
        
        if result['success']:
            print(f"✅ Successfully added {result['added_count']} words to cfg_grammar.py")
            print(f"📝 Backup created at: {result['backup_file']}")
            
            if result['added_words']:
                print(f"\n📋 Added words:")
                for word_type, words in result['added_words'].items():
                    print(f"   {word_type}: {', '.join(words)}")
            
            # Clear approved words from Redis
            cleared = self.redis_manager.clear_approved_words()
            print(f"\n🗑️  Cleared {cleared} approved words from Redis")
        else:
            print(f"❌ Failed to sync: {result.get('error', 'Unknown error')}")
    
    def show_stats(self):
        """Show statistics"""
        summary = self.redis_manager.get_weekly_summary()
        
        print("\n" + "="*60)
        print("📊 Vocabulary Statistics")
        print("="*60)
        print(f"Total Pending:  {summary.get('total_pending', 0)}")
        print("\nBy Type:")
        
        for word_type, count in summary.get('total_by_type', {}).items():
            print(f"  {word_type:15} {count:3}")
        
        print("\n🔥 Top 10 Most Used:")
        for i, word in enumerate(summary.get('most_used', [])[:10], 1):
            print(f"  {i:2}. {word['word']:20} ({word['word_type']:10}) - {word['usage_count']:3}x")
        
        print("="*60 + "\n")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Validation CLI for Bahasa Bali Vocabulary',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          # List all pending words
  %(prog)s list --type Noun              # List pending nouns only
  %(prog)s show ngidang                  # Show details of a word
  %(prog)s approve ngidang               # Approve a word
  %(prog)s reject ngidang                # Reject a word
  %(prog)s approve ngidang tedong ngelah # Approve multiple words
  %(prog)s sync                          # Sync approved words to CFG
  %(prog)s stats                         # Show statistics
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List pending words')
    list_parser.add_argument('--type', help='Filter by word type')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show word details')
    show_parser.add_argument('word', help='Word to show')
    
    # Approve command
    approve_parser = subparsers.add_parser('approve', help='Approve word(s)')
    approve_parser.add_argument('words', nargs='+', help='Word(s) to approve')
    
    # Reject command
    reject_parser = subparsers.add_parser('reject', help='Reject word(s)')
    reject_parser.add_argument('words', nargs='+', help='Word(s) to reject')
    reject_parser.add_argument('--reason', default='', help='Rejection reason')
    
    # Sync command
    subparsers.add_parser('sync', help='Sync approved words to cfg_grammar.py')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ValidationCLI()
    
    # Execute command
    if args.command == 'list':
        cli.list_pending(args.type)
    
    elif args.command == 'show':
        cli.show_details(args.word)
    
    elif args.command == 'approve':
        if len(args.words) == 1:
            cli.approve_word(args.words[0])
        else:
            cli.batch_approve(args.words)
    
    elif args.command == 'reject':
        if len(args.words) == 1:
            cli.reject_word(args.words[0], args.reason)
        else:
            cli.batch_reject(args.words, args.reason)
    
    elif args.command == 'sync':
        cli.sync_to_cfg()
    
    elif args.command == 'stats':
        cli.show_stats()


if __name__ == '__main__':
    main()