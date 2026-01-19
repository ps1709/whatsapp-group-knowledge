# WhatsApp Group Knowledge

Convert your WhatsApp group chats into a searchable Claude Project knowledge base. Perfect for gadget enthusiasts, hobby groups, work teams, or any community that wants to make their collective knowledge accessible via AI.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 What This Does

```
WhatsApp Export (.txt) → Process → Structured Markdown → Claude Project → Shareable Link
```

- **Extracts** messages from WhatsApp chat exports
- **Filters** system messages (joins, media notifications, etc.)
- **Categorizes** discussions by topic (phones, laptops, audio, gaming, etc.)
- **Extracts** product recommendations automatically
- **Organizes** content chronologically for easy reference
- **Outputs** clean markdown ready for Claude Projects

## 🚀 Quick Start

### 1. Export Your WhatsApp Chat

**Android:**
1. Open WhatsApp → Your Group
2. Tap ⋮ → More → Export chat
3. Choose "Without Media"
4. Save the `.txt` file

**iPhone:**
1. Open WhatsApp → Your Group
2. Tap group name → Export Chat
3. Choose "Without Media"
4. Save the `.txt` file

### 2. Process the Export

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/whatsapp-group-knowledge.git
cd whatsapp-group-knowledge

# Run the processor
python whatsapp_processor.py "WhatsApp Chat with My Group.txt"

# Output: WhatsApp Chat with My Group_knowledge_base.md
```

### 3. Create Claude Project

1. Go to [claude.ai/projects](https://claude.ai/projects)
2. Click **+ New Project**
3. Name it (e.g., "Gadgets Group KB")
4. Click the **+** button in Project Knowledge
5. Upload the generated `_knowledge_base.md` file
6. Click **Set project instructions**
7. Paste contents from [`docs/project_instructions.md`](docs/project_instructions.md)
8. Share the project link with your group!

## 📁 Repository Structure

```
whatsapp-group-knowledge/
├── README.md                 # This file
├── whatsapp_processor.py     # Main processing script
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── docs/
│   ├── project_instructions.md   # Claude project instructions template
│   └── setup_guide.md            # Detailed setup guide
└── examples/
    ├── sample_chat.txt           # Sample WhatsApp export
    └── sample_output.md          # Expected output
```

## ⚙️ Configuration

### Customize Topic Keywords

Edit `GADGET_KEYWORDS` in `whatsapp_processor.py` to match your group's interests:

```python
GADGET_KEYWORDS = {
    'phones': ['iphone', 'android', 'pixel', 'samsung', ...],
    'your_topic': ['keyword1', 'keyword2', ...],  # Add custom topics
}
```

### Supported Languages

The processor handles English by default. For other languages, add keywords:

```python
'phones': ['iphone', 'android', 'फोन', 'mobile', ...],  # Hindi
```

## 🔄 Keeping It Updated

Run the processor weekly/monthly with fresh exports:

```bash
# Export new chat from WhatsApp
python whatsapp_processor.py "WhatsApp Chat with My Group.txt" kb_2025_01_20.md

# In Claude Project:
# 1. Delete old knowledge base file
# 2. Upload new file
# The shareable link stays the same!
```

## 📋 Requirements

- Python 3.7+
- No external dependencies (uses standard library only)
- Claude Pro/Team account (for Projects feature)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for use with [Claude](https://claude.ai) by Anthropic
- Inspired by the need to make group knowledge searchable

## 📬 Support

If you encounter any issues or have questions:

1. Check the [Setup Guide](docs/setup_guide.md)
2. Open an [Issue](https://github.com/YOUR_USERNAME/whatsapp-group-knowledge/issues)

---

**Made with ❤️ for gadget enthusiasts and knowledge sharers everywhere**
