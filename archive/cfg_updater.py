import os
import shutil
from datetime import datetime
from typing import Dict, List
import re
from redis_manager import get_redis_manager


class CFGUpdater:
    def __init__(self, cfg_file_path: str = "cfg_grammar.py"):
        self.cfg_file_path = cfg_file_path
        self.redis_manager = get_redis_manager()
        self.backup_dir = "backups"
    
    def create_backup(self) -> str:
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f"cfg_grammar_backup_{timestamp}.py")
        
        shutil.copy2(self.cfg_file_path, backup_file)
        print(f"✅ Backup created: {backup_file}")
        
        return backup_file
    
    def get_approved_words(self) -> Dict[str, List[str]]:

        all_pending = self.redis_manager.get_all_pending_words()
        
        approved_by_type = {}
        for word_data in all_pending:
            if word_data.get('status') == 'approved':
                word_type = word_data['word_type']
                word = word_data['word']
                
                if word_type not in approved_by_type:
                    approved_by_type[word_type] = []
                
                approved_by_type[word_type].append(word)
        
        return approved_by_type
    
    def read_cfg_file(self) -> str:
        with open(self.cfg_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_word_list(self, content: str, word_type: str) -> List[str]:
        # Pattern to match the word type array
        pattern = rf'"{word_type}":\s*\[(.*?)\]'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            return []
        
        # Extract words from [["word1"], ["word2"], ...]
        words_str = match.group(1)
        word_pattern = r'\["([^"]+)"\]'
        words = re.findall(word_pattern, words_str)
        
        return words
    
    def insert_words(self, content: str, word_type: str, new_words: List[str]) -> str:
        # Find the line with word_type
        pattern = rf'("{word_type}":\s*\[)(.*?)(\])'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print(f"⚠️  Word type '{word_type}' not found in cfg_grammar.py")
            return content
        
        # Get existing words section
        before = match.group(1)
        existing = match.group(2)
        after = match.group(3)
        
        # Parse existing words to find the last word format
        # Format: [["word1"], ["word2"], ... , ["wordN"]]
        
        # If there are existing words, we need to add comma
        if existing.strip():
            # Remove trailing whitespace and comma
            existing = existing.rstrip().rstrip(',')
            
            # Add new words
            new_entries = ', '.join([f'["{word}"]' for word in new_words])
            updated = f"{existing}, {new_entries}"
        else:
            # If empty, just add new words
            new_entries = ', '.join([f'["{word}"]' for word in new_words])
            updated = new_entries
        
        # Reconstruct the section
        new_section = f"{before}{updated}{after}"
        
        # Replace in content
        updated_content = content[:match.start()] + new_section + content[match.end():]
        
        return updated_content
    
    def add_update_comment(self, content: str, added_words: Dict[str, List[str]]) -> str:
        """
        Add comment at the top of file documenting the update
        
        Args:
            content: File content
            added_words: Dictionary of added words by type
            
        Returns:
            Content with added comment
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        comment = f"""# Last updated: {timestamp}
# Auto-generated update from Validation Agent
# Added {sum(len(words) for words in added_words.values())} new words
# Categories: {', '.join(f'{k}({len(v)})' for k, v in added_words.items())}

"""
        
        # Find the start of RULES_CFG
        rules_start = content.find('RULES_CFG')
        
        if rules_start > 0:
            # Insert comment before RULES_CFG
            return content[:rules_start] + comment + content[rules_start:]
        else:
            # If RULES_CFG not found, add at the beginning
            return comment + content
    
    def sync_approved_words(self) -> Dict:
        """
        Main function to sync approved words to cfg_grammar.py
        
        Returns:
            Dictionary with sync results
        """
        print("\n" + "="*60)
        print("🔄 Starting CFG Grammar Sync")
        print("="*60 + "\n")
        
        # Get approved words
        approved_words = self.get_approved_words()
        
        if not approved_words:
            return {
                'success': False,
                'error': 'No approved words to sync'
            }
        
        print(f"📋 Found approved words:")
        for word_type, words in approved_words.items():
            print(f"   {word_type}: {len(words)} words - {', '.join(words)}")
        
        print()
        
        # Create backup
        backup_file = self.create_backup()
        
        try:
            # Read current content
            content = self.read_cfg_file()
            
            # Track actually added words (excluding duplicates)
            actually_added = {}
            
            # For each word type, add new words
            for word_type, new_words in approved_words.items():
                # Get existing words
                existing_words = self.extract_word_list(content, word_type)
                
                # Filter out duplicates
                words_to_add = [w for w in new_words if w not in existing_words]
                
                if words_to_add:
                    print(f"➕ Adding {len(words_to_add)} words to {word_type}...")
                    content = self.insert_words(content, word_type, words_to_add)
                    actually_added[word_type] = words_to_add
                else:
                    print(f"ℹ️  All {word_type} words already exist (skipped)")
            
            if not actually_added:
                print("\n⚠️  No new words to add (all already exist)")
                return {
                    'success': False,
                    'error': 'All words already exist in cfg_grammar.py'
                }
            
            # Add update comment
            content = self.add_update_comment(content, actually_added)
            
            # Write updated content
            with open(self.cfg_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n✅ Successfully updated {self.cfg_file_path}")
            print(f"📊 Total words added: {sum(len(w) for w in actually_added.values())}")
            
            return {
                'success': True,
                'backup_file': backup_file,
                'added_words': actually_added,
                'added_count': sum(len(w) for w in actually_added.values())
            }
            
        except Exception as e:
            print(f"\n❌ Error during sync: {e}")
            print(f"⚠️  Restoring from backup...")
            
            # Restore from backup
            shutil.copy2(backup_file, self.cfg_file_path)
            print(f"✅ Restored from backup")
            
            return {
                'success': False,
                'error': str(e)
            }


def test_updater():
    """Test function"""
    updater = CFGUpdater()
    
    # Test with sample data
    print("Testing CFG Updater...\n")
    
    # Get approved words
    approved = updater.get_approved_words()
    print(f"Approved words: {approved}\n")
    
    if approved:
        # Read current file
        content = updater.read_cfg_file()
        print(f"File read successfully: {len(content)} characters\n")
        
        # Test extraction
        for word_type in approved.keys():
            existing = updater.extract_word_list(content, word_type)
            print(f"{word_type} - Existing words: {len(existing)}")
            print(f"   First 5: {existing[:5]}\n")


if __name__ == '__main__':
    test_updater()