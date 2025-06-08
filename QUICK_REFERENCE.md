# Qwen Filesystem Integration - Quick Reference

## 🚀 Getting Started

### Initial Setup (One-time)
```bash
cd /Users/admin/Documents/Qwen_Coder_Local
chmod +x *.sh
./setup_venv.sh
```

### Running the Assistant
```bash
# Option 1: One-click run
./run_qwen.sh

# Option 2: Manual
source venv/bin/activate
cd src && python qwen_filesystem_integration.py
```

## 🎯 LMStudio Requirements
- ✅ Server running on `localhost:1234`
- ✅ Qwen2.5-Coder-1.5B model loaded
- ✅ Function calling enabled

## 💬 Chat Commands
- `help` - Show available commands
- `clear` - Clear conversation history  
- `quit` - Exit the assistant

## 📁 Example Requests
- "List all files in the current directory"
- "Create a Python script that prints hello world"
- "Read the contents of README.md"
- "Search for all .py files in the project"
- "Create a new directory called test_folder"

## 🔒 Security
Access restricted to:
- `/Users/admin/Documents/Qwen_Coder_Local`
- `/Users/admin/Documents/test_workspace`
- `/Users/admin/Desktop/qwen_workspace`

## 🛠️ Available Operations
- **Files**: read, write, append, delete, copy, move
- **Directories**: list, create, delete
- **Search**: find files, get file info
- **Security**: path validation, directory restrictions
