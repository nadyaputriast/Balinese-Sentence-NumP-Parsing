import schedule
import time
from datetime import datetime
from typing import Dict, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import json

from redis_manager import get_redis_manager


class ValidationAgent:  
    def __init__(self):
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_sender = os.getenv('EMAIL_SENDER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.email_recipient = os.getenv('EMAIL_RECIPIENT', '')
        
        # WhatsApp configuration (using Fonnte)
        self.whatsapp_enabled = os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true'
        self.fonnte_token = os.getenv('FONNTE_TOKEN', '')
        self.whatsapp_recipient = os.getenv('WHATSAPP_RECIPIENT', '')
        
        self.redis_manager = get_redis_manager()
    
    def generate_html_report(self, summary: Dict) -> str:
        total = summary.get('total_pending', 0)
        by_type = summary.get('total_by_type', {})
        most_used = summary.get('most_used', [])
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 5px;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
        }}
        .section {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            color: #667eea;
            margin-top: 0;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .word-list {{
            list-style: none;
            padding: 0;
        }}
        .word-item {{
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #28a745;
        }}
        .word-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .word-name {{
            font-weight: bold;
            font-size: 18px;
            color: #333;
        }}
        .word-type {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
        }}
        .word-stats {{
            display: flex;
            gap: 15px;
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}
        .word-notes {{
            font-style: italic;
            color: #555;
            margin-top: 8px;
            padding: 8px;
            background: white;
            border-radius: 3px;
        }}
        .action-buttons {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
        }}
        .btn-approve {{
            background: #28a745;
            color: white;
        }}
        .btn-reject {{
            background: #dc3545;
            color: white;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Laporan Validasi Vocabulary Mingguan</h1>
        <p>Periode: {datetime.now().strftime('%d %B %Y')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total Kata Pending</div>
        </div>
"""
        
        # Add stats by type
        for word_type, count in by_type.items():
            html += f"""
        <div class="stat-card">
            <div class="stat-number">{count}</div>
            <div class="stat-label">{word_type}</div>
        </div>
"""
        
        html += """
    </div>
"""
        
        # Add most used words section
        if most_used:
            html += """
    <div class="section">
        <h2>🔥 Kata Paling Sering Digunakan</h2>
        <ul class="word-list">
"""
            for word_data in most_used:
                word = word_data['word']
                word_type = word_data['word_type']
                usage = word_data['usage_count']
                notes = word_data.get('notes', '-')
                submitted_at = datetime.fromisoformat(word_data['submitted_at']).strftime('%d/%m/%Y %H:%M')
                
                html += f"""
            <li class="word-item">
                <div class="word-header">
                    <span class="word-name">{word}</span>
                    <span class="word-type">{word_type}</span>
                </div>
                <div class="word-stats">
                    <span>📊 Digunakan: <strong>{usage}x</strong></span>
                    <span>📅 Submitted: {submitted_at}</span>
                </div>
                {f'<div class="word-notes">💭 {notes}</div>' if notes != '-' else ''}
            </li>
"""
            
            html += """
        </ul>
    </div>
"""
        
        # Add words grouped by type
        for word_type, words in summary.get('by_type', {}).items():
            if words:
                html += f"""
    <div class="section">
        <h2>📚 {word_type} ({len(words)} kata)</h2>
        <ul class="word-list">
"""
                for word_data in words:
                    word = word_data['word']
                    usage = word_data['usage_count']
                    notes = word_data.get('notes', '-')
                    submitted_at = datetime.fromisoformat(word_data['submitted_at']).strftime('%d/%m/%Y %H:%M')
                    
                    html += f"""
            <li class="word-item">
                <div class="word-header">
                    <span class="word-name">{word}</span>
                </div>
                <div class="word-stats">
                    <span>📊 Digunakan: <strong>{usage}x</strong></span>
                    <span>📅 Submitted: {submitted_at}</span>
                </div>
                {f'<div class="word-notes">💭 {notes}</div>' if notes != '-' else ''}
            </li>
"""
                
                html += """
        </ul>
    </div>
"""
        
        # Add action instructions
        html += """
    <div class="action-buttons">
        <h3>🎯 Instruksi Validasi:</h3>
        <ol>
            <li>Review setiap kata di atas</li>
            <li>Untuk kata yang VALID: Approve dan akan otomatis masuk ke cfg_grammar.py</li>
            <li>Untuk kata yang INVALID: Reject dengan alasan</li>
            <li>Gunakan validation dashboard atau CLI tools</li>
        </ol>
        <p><strong>⏰ Deadline:</strong> Validasi sebelum Minggu depan untuk update weekly</p>
    </div>
    
    <div class="footer">
        <p>📧 Email dikirim otomatis oleh Validation Agent</p>
        <p>Bahasa Bali Parser System - Putu Nadya Putri Astina</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_whatsapp_message(self, summary: Dict) -> str:
        total = summary.get('total_pending', 0)
        by_type = summary.get('total_by_type', {})
        most_used = summary.get('most_used', [])[:5]  # Top 5 only for WhatsApp
        
        message = f"""
📊 *LAPORAN VALIDASI VOCABULARY MINGGUAN*
Periode: {datetime.now().strftime('%d %B %Y')}

━━━━━━━━━━━━━━━━━━━━

📈 *STATISTIK*
• Total Kata Pending: *{total}*
"""
        
        for word_type, count in by_type.items():
            message += f"• {word_type}: {count}\n"
        
        message += "\n━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if most_used:
            message += "🔥 *TOP 5 KATA PALING SERING DIGUNAKAN:*\n\n"
            for i, word_data in enumerate(most_used, 1):
                word = word_data['word']
                word_type = word_data['word_type']
                usage = word_data['usage_count']
                message += f"{i}. *{word}* ({word_type})\n"
                message += f"   📊 {usage}x digunakan\n\n"
        
        message += "━━━━━━━━━━━━━━━━━━━━\n\n"
        message += "⏰ *Action Required:*\n"
        message += "Silakan cek email untuk detail lengkap dan lakukan validasi.\n\n"
        message += "✅ Approve kata yang valid\n"
        message += "❌ Reject kata yang invalid\n\n"
        message += "🔗 Link validation dashboard akan dikirim via email.\n"
        
        return message
    
    def send_email(self, summary: Dict) -> bool:
        """
        Send email report to validator
        
        Args:
            summary: Dictionary with weekly summary data
            
        Returns:
            True if successful
        """
        if not self.email_sender or not self.email_recipient:
            print("⚠️ Email configuration not set")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Laporan Validasi Vocabulary - {datetime.now().strftime('%d %B %Y')}"
            msg['From'] = self.email_sender
            msg['To'] = self.email_recipient
            
            # Generate HTML content
            html_content = self.generate_html_report(summary)
            
            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {self.email_recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_whatsapp(self, summary: Dict) -> bool:
        """
        Send WhatsApp message to validator using Fonnte
        
        Args:
            summary: Dictionary with weekly summary data
            
        Returns:
            True if successful
        """
        if not self.whatsapp_enabled or not self.fonnte_token:
            print("⚠️ WhatsApp/Fonnte not configured")
            return False
        
        try:
            # Generate message
            message = self.generate_whatsapp_message(summary)
            
            # Send via Fonnte API
            url = "https://api.fonnte.com/send"
            
            headers = {
                'Authorization': self.fonnte_token
            }
            
            data = {
                'target': self.whatsapp_recipient,
                'message': message,
                'countryCode': '62'  # Indonesia country code
            }
            
            response = requests.post(url, headers=headers, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    print(f"✅ WhatsApp sent successfully to {self.whatsapp_recipient}")
                    print(f"   Message ID: {result.get('id', 'N/A')}")
                    return True
                else:
                    print(f"❌ WhatsApp failed: {result.get('reason', 'Unknown error')}")
                    return False
            else:
                print(f"❌ WhatsApp HTTP error: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            
        except Exception as e:
            print(f"❌ Error sending WhatsApp: {e}")
            return False
    
    def run_weekly_validation(self):
        """Run the weekly validation process"""
        print("\n" + "="*50)
        print(f"🤖 Running Weekly Validation Agent")
        print(f"📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}")
        print("="*50 + "\n")
        
        # Get summary from Redis
        summary = self.redis_manager.get_weekly_summary()
        
        if summary.get('total_pending', 0) == 0:
            print("ℹ️ No pending words to validate")
            return
        
        print(f"📊 Total pending words: {summary['total_pending']}")
        
        # Send email
        print("\n📧 Sending email report...")
        email_sent = self.send_email(summary)
        
        # Send WhatsApp (optional)
        if self.whatsapp_enabled:
            print("\n📱 Sending WhatsApp notification...")
            whatsapp_sent = self.send_whatsapp(summary)
        
        print("\n" + "="*50)
        print("✅ Weekly validation process completed")
        print("="*50 + "\n")
    
    def start_scheduler(self):
        """Start the weekly scheduler"""
        # Schedule untuk setiap Senin jam 09:00
        schedule.every().monday.at("09:00").do(self.run_weekly_validation)
        
        # Alternatif: setiap minggu
        # schedule.every().week.do(self.run_weekly_validation)
        
        print("🚀 Validation Agent Started")
        print("📅 Scheduled: Every Monday at 09:00")
        print("⏳ Waiting for next run...\n")
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour


def run_agent():
    """Main function to run the validation agent"""
    agent = ValidationAgent()
    agent.start_scheduler()


if __name__ == "__main__":
    # For testing, run immediately
    agent = ValidationAgent()
    agent.run_weekly_validation()