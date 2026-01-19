# Contributing to WhatsApp Group Knowledge

First off, thank you for considering contributing! 🎉

## How Can I Contribute?

### Reporting Bugs

- Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include sample input (with personal info removed)
- Include the full error message
- Specify your Python version and OS

### Suggesting Features

- Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case clearly
- Consider if it fits the project scope

### Pull Requests

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run with sample chat
   python whatsapp_processor.py examples/sample_chat.txt test_output.md -v
   ```

5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**

## Code Style

- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Use type hints where helpful

## Areas We'd Love Help With

- 🌍 **Internationalization**: Support for more languages and date formats
- 📊 **Analytics**: Better topic detection and statistics
- 🧪 **Testing**: Unit tests for parser functions
- 📖 **Documentation**: Tutorials, video guides, translations
- 🎨 **Output formats**: Different markdown styles, HTML output

## Questions?

Open an issue with the "question" label or start a discussion.

Thanks for helping make this project better! 🙏
