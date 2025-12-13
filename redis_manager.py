from upstash_redis import Redis
import json
from datetime import datetime
from typing import Dict, List, Optional
import os

class RedisVocabManager:
    """Manages pending vocabulary in Redis"""
    
    def __init__(self):
        """Initialize Redis connection"""
        # Konfigurasi Upstash Redis (dari environment variable)
        self.redis_url = os.getenv('UPSTASH_REDIS_URL', 'https://civil-mongoose-20933.upstash.io')
        self.redis_token = os.getenv('UPSTASH_REDIS_TOKEN', 'AVHFAAIncDIwMDkzNTg5MGQ5ZTM0NmEwYmI3ODZjMWM1NDIxZWVhYXAyMjA5MzM')
        
        # Connect to Upstash Redis
        try:
            self.redis_client = Redis(
                url=self.redis_url,
                token=self.redis_token
            )
            # Test connection
            self.redis_client.ping()
            print("✅ Upstash Redis connection successful")
        except Exception as e:
            print(f"❌ Upstash Redis connection failed: {e}")
            self.redis_client = None
    
    def add_pending_word(self, word: str, word_type: str, notes: str = "", 
                        submitted_by: str = "anonymous") -> bool:
        if not self.redis_client:
            return False
        
        try:
            # Create unique key for this word
            key = f"pending_vocab:{word.lower()}"
            
            # Prepare data
            data = {
                "word": word.lower(),
                "word_type": word_type,
                "notes": notes,
                "submitted_by": submitted_by,
                "submitted_at": datetime.now().isoformat(),
                "status": "pending",
                "usage_count": 0  # Track how many times it's been used
            }
            
            # Save to Redis
            self.redis_client.set(key, json.dumps(data))
            
            # Add to pending list (for easy retrieval)
            self.redis_client.sadd("pending_vocab_list", word.lower())
            
            print(f"✅ Added pending word: {word}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding word: {e}")
            return False
    
    def get_pending_word(self, word: str) -> Optional[Dict]:
        if not self.redis_client:
            return None
        
        try:
            key = f"pending_vocab:{word.lower()}"
            data = self.redis_client.get(key)
            
            if data:
                return json.loads(data)
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving word: {e}")
            return None
    
    def get_all_pending_words(self) -> List[Dict]:
        if not self.redis_client:
            return []
        
        try:
            # Get all pending word keys
            pending_words = self.redis_client.smembers("pending_vocab_list")
            
            results = []
            for word in pending_words:
                data = self.get_pending_word(word)
                if data:
                    results.append(data)
            
            # Sort by submission date (newest first)
            results.sort(key=lambda x: x['submitted_at'], reverse=True)
            return results
            
        except Exception as e:
            print(f"❌ Error retrieving all words: {e}")
            return []
    
    def increment_usage(self, word: str) -> bool:
        if not self.redis_client:
            return False
        
        try:
            data = self.get_pending_word(word)
            if data:
                data['usage_count'] += 1
                key = f"pending_vocab:{word.lower()}"
                self.redis_client.set(key, json.dumps(data))
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error incrementing usage: {e}")
            return False
    
    def check_word_exists(self, word: str, cfg_grammar: Dict) -> tuple:
        word_lower = word.lower()
        
        # Check in CFG Grammar
        exists_in_cfg = False
        for key, values in cfg_grammar.items():
            if key in ['Noun', 'Verb', 'Adj', 'Num', 'PropNoun', 'Pronoun', 
                      'Prep', 'Adv', 'Det']:
                raw_words = [item[0] for item in values]
                if word_lower in raw_words:
                    exists_in_cfg = True
                    break
        
        # Check in Redis
        word_data = self.get_pending_word(word_lower)
        exists_in_redis = word_data is not None
        
        return exists_in_cfg, exists_in_redis, word_data
    
    def approve_word(self, word: str) -> bool:
        if not self.redis_client:
            return False
        
        try:
            data = self.get_pending_word(word)
            if data:
                data['status'] = 'approved'
                data['approved_at'] = datetime.now().isoformat()
                key = f"pending_vocab:{word.lower()}"
                self.redis_client.set(key, json.dumps(data))
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error approving word: {e}")
            return False
    
    def reject_word(self, word: str, reason: str = "") -> bool:
        if not self.redis_client:
            return False
        
        try:
            key = f"pending_vocab:{word.lower()}"
            
            # Log rejection (optional)
            data = self.get_pending_word(word)
            if data:
                data['status'] = 'rejected'
                data['rejection_reason'] = reason
                data['rejected_at'] = datetime.now().isoformat()
                
                # Save to rejection log
                rejection_key = f"rejected_vocab:{word.lower()}:{datetime.now().timestamp()}"
                self.redis_client.set(rejection_key, json.dumps(data))
                self.redis_client.expire(rejection_key, 2592000)  # Keep for 30 days
            
            # Remove from pending
            self.redis_client.delete(key)
            self.redis_client.srem("pending_vocab_list", word.lower())
            
            return True
            
        except Exception as e:
            print(f"❌ Error rejecting word: {e}")
            return False
    
    def get_weekly_summary(self) -> Dict:
        if not self.redis_client:
            return {}
        
        try:
            all_pending = self.get_all_pending_words()
            
            # Group by word type
            by_type = {}
            for word in all_pending:
                word_type = word['word_type']
                if word_type not in by_type:
                    by_type[word_type] = []
                by_type[word_type].append(word)
            
            # Sort each type by usage count
            for word_type in by_type:
                by_type[word_type].sort(key=lambda x: x['usage_count'], reverse=True)
            
            summary = {
                "total_pending": len(all_pending),
                "by_type": by_type,
                "total_by_type": {k: len(v) for k, v in by_type.items()},
                "most_used": sorted(all_pending, key=lambda x: x['usage_count'], reverse=True)[:10],
                "generated_at": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return {}
    
    def clear_approved_words(self) -> int:
        if not self.redis_client:
            return 0
        
        try:
            all_pending = self.get_all_pending_words()
            cleared = 0
            
            for word_data in all_pending:
                if word_data.get('status') == 'approved':
                    word = word_data['word']
                    key = f"pending_vocab:{word}"
                    self.redis_client.delete(key)
                    self.redis_client.srem("pending_vocab_list", word)
                    cleared += 1
            
            return cleared
            
        except Exception as e:
            print(f"❌ Error clearing approved words: {e}")
            return 0


# Singleton instance
_redis_manager = None

def get_redis_manager() -> RedisVocabManager:
    """Get or create Redis manager instance"""
    global _redis_manager
    if _redis_manager is None:
        _redis_manager = RedisVocabManager()
    return _redis_manager