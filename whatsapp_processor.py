#!/usr/bin/env python3
"""
WhatsApp Chat Processor for Claude Projects
============================================

Converts WhatsApp chat exports to structured markdown knowledge base
suitable for upload to Claude Projects.

Usage:
    python whatsapp_processor.py <input_file.txt> [output_file.md]
    
Examples:
    python whatsapp_processor.py "WhatsApp Chat with Gadget Gang.txt"
    python whatsapp_processor.py chat.txt gadgets_kb.md
    python whatsapp_processor.py chat.txt --topics phones,laptops

Author: Your Name
License: MIT
"""

import re
import sys
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple


# =============================================================================
# CONFIGURATION - Customize these for your group
# =============================================================================

# WhatsApp export date/time patterns (supports multiple formats)
MESSAGE_PATTERNS = [
    # Format: [DD/MM/YYYY, HH:MM:SS] Sender: Message
    r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\]\s*([^:]+):\s*(.+)$',
    # Format: DD/MM/YYYY, HH:MM - Sender: Message
    r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)$',
    # Format: MM/DD/YY, HH:MM - Sender: Message (US format)
    r'^(\d{1,2}/\d{1,2}/\d{2}),\s*(\d{1,2}:\d{2}(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)$',
    # Format: YYYY-MM-DD HH:MM - Sender: Message (ISO format)
    r'^(\d{4}-\d{2}-\d{2}),?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*([^:]+):\s*(.+)$',
]

# System messages to filter out
SYSTEM_MESSAGE_PATTERNS = [
    r'Messages and calls are end-to-end encrypted',
    r'created group',
    r'added you',
    r'left$',
    r'removed',
    r'changed the subject',
    r'changed this group',
    r'changed the group',
    r'security code changed',
    r'joined using this group',
    r"You're now an admin",
    r'is now an admin',
    r'<Media omitted>',
    r'image omitted',
    r'video omitted',
    r'audio omitted',
    r'sticker omitted',
    r'GIF omitted',
    r'Contact card omitted',
    r'document omitted',
    r'This message was deleted',
    r'You deleted this message',
    r'Waiting for this message',
    r'null',
]

# Topic keywords for categorization
# Customize this dictionary for your group's interests
TOPIC_KEYWORDS = {
    'phones': [
        'iphone', 'android', 'pixel', 'samsung', 'oneplus', 'xiaomi', 
        'phone', 'smartphone', 'mobile', 'nothing phone', 'motorola',
        'oppo', 'vivo', 'realme', 'poco', 'redmi', 'galaxy'
    ],
    'laptops': [
        'laptop', 'macbook', 'thinkpad', 'dell', 'hp', 'asus', 'lenovo',
        'notebook', 'ultrabook', 'chromebook', 'surface laptop', 'xps',
        'ideapad', 'pavilion', 'inspiron', 'vivobook', 'zenbook'
    ],
    'audio': [
        'headphones', 'earbuds', 'airpods', 'speaker', 'soundbar', 'audio',
        'sony wh', 'bose', 'sennheiser', 'jabra', 'jbl', 'marshall',
        'tws', 'wireless earbuds', 'anc', 'noise cancelling', 'dac', 'amp'
    ],
    'wearables': [
        'watch', 'smartwatch', 'apple watch', 'fitbit', 'garmin', 'band',
        'ring', 'oura', 'whoop', 'galaxy watch', 'amazfit', 'mi band'
    ],
    'tablets': [
        'ipad', 'tablet', 'surface', 'tab', 'galaxy tab', 'fire tablet',
        'kindle', 'e-reader', 'remarkable'
    ],
    'gaming': [
        'ps5', 'xbox', 'switch', 'nintendo', 'gaming', 'controller',
        'console', 'steam deck', 'rog', 'playstation', 'gpu', 'graphics card',
        'rtx', 'gaming laptop', 'gaming pc', 'mechanical keyboard'
    ],
    'cameras': [
        'camera', 'dslr', 'mirrorless', 'gopro', 'drone', 'dji',
        'sony alpha', 'canon', 'nikon', 'fujifilm', 'lens', 'photography'
    ],
    'smart_home': [
        'alexa', 'echo', 'google home', 'nest', 'smart home', 'ring doorbell',
        'hue', 'smart bulb', 'smart plug', 'home assistant', 'homekit',
        'smart lock', 'thermostat', 'robot vacuum', 'roomba'
    ],
    'accessories': [
        'charger', 'cable', 'case', 'stand', 'dock', 'hub', 'adapter',
        'power bank', 'usb-c', 'wireless charger', 'magsafe', 'screen protector'
    ],
    'deals': [
        'deal', 'sale', 'discount', 'offer', 'price drop', 'amazon',
        'flipkart', 'best buy', 'coupon', 'cashback', 'prime day', 'black friday'
    ],
    'troubleshooting': [
        'problem', 'issue', 'fix', 'help', 'not working', 'error', 'broken',
        'bug', 'crash', 'slow', 'battery drain', 'overheating', 'repair'
    ],
}


# =============================================================================
# PARSER FUNCTIONS
# =============================================================================

def parse_message(line: str, compiled_patterns: List) -> Optional[Dict]:
    """Try to parse a line as a WhatsApp message."""
    for pattern in compiled_patterns:
        match = pattern.match(line)
        if match:
            return {
                'date': match.group(1),
                'time': match.group(2),
                'sender': match.group(3).strip(),
                'message': match.group(4).strip()
            }
    return None


def is_system_message(message: str) -> bool:
    """Check if a message is a system message to filter out."""
    for pattern in SYSTEM_MESSAGE_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False


def detect_topics(message: str, keywords_dict: Dict = None) -> List[str]:
    """Detect topics in a message based on keywords."""
    if keywords_dict is None:
        keywords_dict = TOPIC_KEYWORDS
    
    message_lower = message.lower()
    topics = []
    for topic, keywords in keywords_dict.items():
        if any(kw in message_lower for kw in keywords):
            topics.append(topic)
    return topics


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object."""
    formats = [
        '%d/%m/%Y', '%d/%m/%y', '%m/%d/%Y', '%m/%d/%y',
        '%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


# =============================================================================
# PROCESSING FUNCTIONS
# =============================================================================

def process_chat(input_file: str) -> List[Dict]:
    """Process WhatsApp chat export file."""
    compiled_patterns = [re.compile(p, re.MULTILINE) for p in MESSAGE_PATTERNS]
    
    messages = []
    current_message = None
    
    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    content = None
    
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                content = f.readlines()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise ValueError(f"Could not decode file with supported encodings: {encodings}")
    
    for line in content:
        line = line.strip()
        if not line:
            continue
        
        parsed = parse_message(line, compiled_patterns)
        
        if parsed:
            # Save previous message if exists
            if current_message and not is_system_message(current_message['message']):
                messages.append(current_message)
            current_message = parsed
        elif current_message:
            # Continuation of previous message (multi-line)
            current_message['message'] += '\n' + line
    
    # Don't forget the last message
    if current_message and not is_system_message(current_message['message']):
        messages.append(current_message)
    
    return messages


def group_by_topic(messages: List[Dict]) -> Tuple[Dict[str, List], List]:
    """Group messages by detected topics."""
    topic_messages = defaultdict(list)
    general_messages = []
    
    for msg in messages:
        topics = detect_topics(msg['message'])
        if topics:
            for topic in topics:
                topic_messages[topic].append(msg)
        else:
            general_messages.append(msg)
    
    return dict(topic_messages), general_messages


def group_by_date(messages: List[Dict]) -> Dict[str, List]:
    """Group messages by month/year."""
    date_groups = defaultdict(list)
    
    for msg in messages:
        parsed_date = parse_date(msg['date'])
        if parsed_date:
            key = parsed_date.strftime('%Y-%m')
        else:
            key = 'unknown'
        date_groups[key].append(msg)
    
    return dict(sorted(date_groups.items(), reverse=True))


def extract_recommendations(messages: List[Dict]) -> List[Dict]:
    """Extract product recommendations from messages."""
    recommendations = []
    rec_patterns = [
        r'(?:recommend|suggesting|suggest|try|get|buy|go for|best|loving|love my)\s+(?:the\s+)?([A-Z][A-Za-z0-9\s\-]+)',
        r'([A-Z][A-Za-z0-9\s\-]+)\s+(?:is|are)\s+(?:great|amazing|awesome|good|best|worth|excellent|fantastic)',
        r'(?:just got|picked up|bought|ordered)\s+(?:a\s+|the\s+)?([A-Z][A-Za-z0-9\s\-]+)',
    ]
    
    for msg in messages:
        for pattern in rec_patterns:
            matches = re.findall(pattern, msg['message'])
            for match in matches:
                match = match.strip()
                # Filter out common false positives
                if len(match) > 3 and len(match) < 50:
                    if not any(word in match.lower() for word in ['the', 'this', 'that', 'what', 'which']):
                        recommendations.append({
                            'product': match,
                            'by': msg['sender'],
                            'date': msg['date'],
                            'context': msg['message'][:200]
                        })
    
    return recommendations


def get_participant_stats(messages: List[Dict]) -> Dict[str, Dict]:
    """Get statistics for each participant."""
    stats = defaultdict(lambda: {'count': 0, 'topics': defaultdict(int)})
    
    for msg in messages:
        sender = msg['sender']
        stats[sender]['count'] += 1
        for topic in detect_topics(msg['message']):
            stats[sender]['topics'][topic] += 1
    
    return dict(stats)


# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def generate_markdown(messages: List[Dict], input_filename: str, 
                      title: str = None) -> str:
    """Generate structured markdown output."""
    topic_messages, general_messages = group_by_topic(messages)
    date_groups = group_by_date(messages)
    recommendations = extract_recommendations(messages)
    participant_stats = get_participant_stats(messages)
    
    # Get unique participants
    participants = sorted(set(msg['sender'] for msg in messages))
    
    # Get date range
    dates = [parse_date(msg['date']) for msg in messages]
    dates = [d for d in dates if d]
    if dates:
        date_range = f"{min(dates).strftime('%B %Y')} - {max(dates).strftime('%B %Y')}"
    else:
        date_range = "Unknown"
    
    # Build markdown
    md = []
    
    # Title
    kb_title = title or "Group Knowledge Base"
    md.append(f"# {kb_title}")
    md.append(f"\n**Source:** {input_filename}")
    md.append(f"**Date Range:** {date_range}")
    md.append(f"**Total Messages:** {len(messages):,}")
    md.append(f"**Participants:** {len(participants)}")
    md.append(f"\n---\n")
    
    # Table of Contents
    md.append("## Table of Contents\n")
    md.append("1. [Quick Stats](#quick-stats)")
    md.append("2. [Topic Discussions](#topic-discussions)")
    md.append("3. [Product Recommendations](#product-recommendations)")
    md.append("4. [Recent Discussions](#recent-discussions)")
    md.append("5. [Participant Expertise](#participant-expertise)")
    md.append("6. [Full Archive](#full-archive-by-date)")
    md.append("\n---\n")
    
    # Quick Stats
    md.append("## Quick Stats\n")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| Total Messages | {len(messages):,} |")
    md.append(f"| Date Range | {date_range} |")
    md.append(f"| Active Members | {len(participants)} |")
    md.append(f"| Topics Covered | {len(topic_messages)} |")
    md.append(f"| Product Mentions | {len(recommendations)} |")
    md.append("")
    
    # Topic Discussions
    md.append("\n## Topic Discussions\n")
    for topic, msgs in sorted(topic_messages.items(), key=lambda x: -len(x[1])):
        topic_title = topic.replace('_', ' ').title()
        emoji_map = {
            'phones': '📱', 'laptops': '💻', 'audio': '🎧', 
            'wearables': '⌚', 'tablets': '📱', 'gaming': '🎮',
            'cameras': '📷', 'smart_home': '🏠', 'accessories': '🔌',
            'deals': '💰', 'troubleshooting': '🔧'
        }
        emoji = emoji_map.get(topic, '📌')
        
        md.append(f"### {emoji} {topic_title} ({len(msgs)} messages)\n")
        
        # Show recent discussions (last 5)
        recent_msgs = msgs[-5:]
        for msg in recent_msgs:
            clean_msg = msg['message'][:300].replace('\n', ' ')
            if len(msg['message']) > 300:
                clean_msg += '...'
            md.append(f"- **{msg['sender']}** ({msg['date']}): {clean_msg}")
        md.append("")
    
    # Product Recommendations
    md.append("\n## Product Recommendations\n")
    if recommendations:
        seen = set()
        unique_recs = []
        for rec in recommendations:
            key = rec['product'].lower()
            if key not in seen:
                seen.add(key)
                unique_recs.append(rec)
        
        for rec in unique_recs[:25]:  # Top 25
            md.append(f"- **{rec['product']}** — mentioned by {rec['by']} ({rec['date']})")
    else:
        md.append("*No explicit recommendations detected. Search the archive for specific products.*")
    md.append("")
    
    # Recent Discussions
    md.append("\n## Recent Discussions\n")
    recent_months = list(date_groups.items())[:2]  # Last 2 months
    for month_key, month_msgs in recent_months:
        try:
            month_display = datetime.strptime(month_key, '%Y-%m').strftime('%B %Y')
        except:
            month_display = month_key
        
        md.append(f"### {month_display}\n")
        for msg in month_msgs[-15:]:  # Last 15 messages
            clean_msg = msg['message'].replace('\n', ' ')[:200]
            md.append(f"**{msg['sender']}** ({msg['date']} {msg['time']})")
            md.append(f"> {clean_msg}\n")
    
    # Participant Expertise
    md.append("\n## Participant Expertise\n")
    md.append("*Who knows what — based on discussion frequency*\n")
    
    for sender, stats in sorted(participant_stats.items(), key=lambda x: -x[1]['count'])[:10]:
        top_topics = sorted(stats['topics'].items(), key=lambda x: -x[1])[:3]
        if top_topics:
            topics_str = ', '.join([f"{t[0].replace('_', ' ')}" for t in top_topics])
            md.append(f"- **{sender}** ({stats['count']} msgs): {topics_str}")
        else:
            md.append(f"- **{sender}** ({stats['count']} msgs)")
    md.append("")
    
    # Full Archive
    md.append("\n## Full Archive by Date\n")
    for month_key, month_msgs in date_groups.items():
        try:
            month_display = datetime.strptime(month_key, '%Y-%m').strftime('%B %Y')
        except:
            month_display = month_key
        
        md.append(f"### {month_display} ({len(month_msgs)} messages)\n")
        md.append("<details>")
        md.append(f"<summary>Click to expand {month_display}</summary>\n")
        
        for msg in month_msgs:
            clean_msg = msg['message'].replace('|', '\\|').replace('\n', ' ')
            md.append(f"**{msg['sender']}** ({msg['date']} {msg['time']}): {clean_msg}\n")
        
        md.append("</details>\n")
    
    return '\n'.join(md)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Convert WhatsApp chat exports to Claude Project knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python whatsapp_processor.py "WhatsApp Chat with Gadgets.txt"
  python whatsapp_processor.py chat.txt output.md
  python whatsapp_processor.py chat.txt -t "Gadgets Group KB"
        """
    )
    
    parser.add_argument('input_file', help='WhatsApp chat export file (.txt)')
    parser.add_argument('output_file', nargs='?', help='Output markdown file (optional)')
    parser.add_argument('-t', '--title', help='Knowledge base title', 
                        default='Group Knowledge Base')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Show detailed processing info')
    
    args = parser.parse_args()
    
    input_file = args.input_file
    
    # Default output filename
    if args.output_file:
        output_file = args.output_file
    else:
        output_file = Path(input_file).stem + '_knowledge_base.md'
    
    print(f"📂 Processing: {input_file}")
    
    # Process chat
    try:
        messages = process_chat(input_file)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        sys.exit(1)
    
    print(f"✅ Found {len(messages):,} messages (after filtering system messages)")
    
    if args.verbose:
        topic_messages, _ = group_by_topic(messages)
        print(f"\n📊 Topics detected:")
        for topic, msgs in sorted(topic_messages.items(), key=lambda x: -len(x[1])):
            print(f"   - {topic}: {len(msgs)} messages")
    
    # Generate markdown
    markdown = generate_markdown(messages, Path(input_file).name, args.title)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"📄 Knowledge base created: {output_file}")
    print(f"\n🚀 Next steps:")
    print(f"   1. Go to claude.ai/projects")
    print(f"   2. Create a new project (or open existing)")
    print(f"   3. Click '+' in Project Knowledge")
    print(f"   4. Upload '{output_file}'")
    print(f"   5. Set project instructions (see docs/project_instructions.md)")
    print(f"   6. Share the project link with your group!")


if __name__ == '__main__':
    main()
