# Detailed Setup Guide

Complete guide for setting up WhatsApp Group Knowledge Base.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Exporting WhatsApp Chat](#exporting-whatsapp-chat)
3. [Running the Processor](#running-the-processor)
4. [Creating Claude Project](#creating-claude-project)
5. [Sharing with Group](#sharing-with-group)
6. [Maintenance & Updates](#maintenance--updates)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- Python 3.7 or higher
- WhatsApp account with group access
- Claude account (Free tier works, Pro/Team recommended for sharing)

### Check Python Installation

```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not installed:
# macOS: brew install python3
# Windows: Download from python.org
# Linux: sudo apt install python3
```

---

## Exporting WhatsApp Chat

### Android

1. Open WhatsApp
2. Navigate to your group chat
3. Tap the **⋮** (three dots) menu in the top right
4. Select **More** → **Export chat**
5. Choose **Without Media** (recommended for smaller file size)
6. Share/save the `.txt` file to your computer

### iPhone

1. Open WhatsApp
2. Navigate to your group chat
3. Tap the **group name** at the top
4. Scroll down and tap **Export Chat**
5. Choose **Without Media**
6. Save the `.txt` file

### Tips for Export

- Export **without media** keeps file size manageable
- Larger groups may take a few moments to export
- The export includes all available history (may vary by device)

---

## Running the Processor

### Basic Usage

```bash
# Navigate to the repository
cd whatsapp-group-knowledge

# Run with default settings
python whatsapp_processor.py "WhatsApp Chat with My Group.txt"
```

### Advanced Options

```bash
# Specify custom output filename
python whatsapp_processor.py chat.txt my_knowledge_base.md

# Add custom title
python whatsapp_processor.py chat.txt -t "Gadgets Enthusiasts KB"

# Verbose mode (shows topic breakdown)
python whatsapp_processor.py chat.txt -v
```

### Expected Output

```
📂 Processing: WhatsApp Chat with My Group.txt
✅ Found 1,234 messages (after filtering system messages)
📄 Knowledge base created: WhatsApp Chat with My Group_knowledge_base.md

🚀 Next steps:
   1. Go to claude.ai/projects
   2. Create a new project (or open existing)
   3. Click '+' in Project Knowledge
   4. Upload 'WhatsApp Chat with My Group_knowledge_base.md'
   5. Set project instructions (see docs/project_instructions.md)
   6. Share the project link with your group!
```

---

## Creating Claude Project

### Step 1: Access Projects

1. Go to [claude.ai/projects](https://claude.ai/projects)
2. Sign in to your Claude account

### Step 2: Create New Project

1. Click **+ New Project** in the upper right
2. Enter a name: e.g., "Gadgets Group Knowledge Base"
3. Add description (optional): "Searchable knowledge from our WhatsApp group"
4. Click **Create**

### Step 3: Upload Knowledge Base

1. On the project page, look at the **right side** for "Project knowledge"
2. Click the **+** button
3. Select **Upload files**
4. Choose your generated `_knowledge_base.md` file
5. Wait for upload to complete

### Step 4: Set Project Instructions

1. Click **Set project instructions** (or edit icon)
2. Copy contents from `docs/project_instructions.md`
3. Paste into the instructions field
4. Click **Save**

### Step 5: Test It

Start a new chat in the project and try:
- "What topics has the group discussed?"
- "Who recommends good headphones?"
- "What were recent discussions about?"

---

## Sharing with Group

### For Free Accounts

Free accounts have limited sharing options. Consider upgrading for team features.

### For Pro/Team Accounts

1. Open your project
2. Click **Share project** button
3. Options:
   - **Keep private**: Only you can access
   - **Share with organization**: Everyone in your org can access
   - **Invite specific people**: Add by email

### Sharing via Link

1. Click **Share project**
2. Enable "Anyone with link can chat"
3. Copy the link
4. Share in your WhatsApp group!

### Permission Levels

| Level | Can Do |
|-------|--------|
| **Can use** | View content, chat within project |
| **Can edit** | Modify knowledge, update instructions |

---

## Maintenance & Updates

### Weekly Update Workflow

```
┌────────────────────────────────────────────────────────────┐
│  WEEKLY UPDATE (5-10 minutes)                              │
├────────────────────────────────────────────────────────────┤
│  1. □ Export fresh WhatsApp chat                           │
│  2. □ Run: python whatsapp_processor.py "chat.txt"         │
│  3. □ Go to Claude Project → Project Knowledge             │
│  4. □ Delete old file                                      │
│  5. □ Upload new file                                      │
│  6. □ Done! Link stays the same                            │
└────────────────────────────────────────────────────────────┘
```

### Pro Tips

**Archive old exports:**
```bash
# Keep dated backups
python whatsapp_processor.py chat.txt kb_2025_01_20.md
```

**Incremental updates:**
- For very active groups, keep multiple knowledge files
- Claude will reference all uploaded files

**Set a reminder:**
- Add a recurring calendar event for weekly updates
- Assign a group member as "KB keeper"

---

## Troubleshooting

### "Command not found" error

```bash
# Try python3 instead of python
python3 whatsapp_processor.py chat.txt

# Check Python is installed
which python3
```

### "File not found" error

```bash
# Make sure you're in the right directory
cd whatsapp-group-knowledge

# Check the file path is correct (use quotes for spaces)
python whatsapp_processor.py "WhatsApp Chat with Gadgets Group.txt"
```

### Script can't parse messages

Your WhatsApp may use a different date format. Check the first few lines of your export:

```
# Common formats supported:
[15/01/2025, 10:30:45] Sender: Message
15/01/2025, 10:30 - Sender: Message
01/15/25, 10:30 AM - Sender: Message
```

If your format differs, open an issue on GitHub.

### No messages found

- Ensure you exported as `.txt` not `.zip`
- Check file isn't empty
- Verify encoding (should be UTF-8)

### Claude can't find information

- Make sure the knowledge base file uploaded successfully
- Check if the topic was actually discussed
- Try more specific search terms

### Project Knowledge section not visible

- Make sure you're on the **project overview page**, not inside a chat
- Go to [claude.ai/projects](https://claude.ai/projects) and click your project name
- The knowledge section should be on the right side

---

## Getting Help

1. Check this guide first
2. Look at [examples/](../examples/) folder
3. Open an issue on GitHub with:
   - Error message
   - First few lines of your WhatsApp export
   - Python version (`python --version`)

---

## Next Steps

- Customize `TOPIC_KEYWORDS` for your group's interests
- Add more date formats if needed
- Contribute improvements back to the repository!
