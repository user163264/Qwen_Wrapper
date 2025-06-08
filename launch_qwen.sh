#!/bin/bash
# Qwen Assistant Launcher with System Prompts
# Usage: ./launch_qwen.sh [prompt_name] [--v4]

cd /Users/admin/Documents/Qwen_Coder_Local

echo "🚀 Qwen Assistant Launcher"
echo "📝 With configurable system prompts!"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found!"
    echo "Run: ./setup_venv.sh first"
    exit 1
fi

# Determine version to use
use_v4=false
prompt_arg=""

# Parse arguments
for arg in "$@"; do
    if [ "$arg" = "--v4" ]; then
        use_v4=true
    else
        prompt_arg="$arg"
    fi
done

# Select version
if [ "$use_v4" = true ]; then
    echo "📁 Using V4 (filesystem only)"
    version_script="src/qwen_filesystem_integration_v4.py"
else
    echo "🆕 Using V5 (filesystem + code analysis)"
    version_script="src/qwen_filesystem_integration_v5.py"
fi

# Check for prompt argument
if [ "$prompt_arg" ]; then
    echo "📝 Using system prompt: $prompt_arg"
    python "$version_script" --prompt "$prompt_arg"
else
    echo "📝 Available system prompts:"
    if [ -d "prompts" ]; then
        ls prompts/*.txt 2>/dev/null | sed 's|prompts/||' | sed 's|.txt||' | sed 's|^|  - |'
    fi
    echo ""
    echo "💡 Usage examples:"
    echo "  ./launch_qwen.sh                                # V5 with default enhanced prompt"
    echo "  ./launch_qwen.sh --v4                           # V4 filesystem only"
    echo "  ./launch_qwen.sh system_prompt_coding.txt       # V5 with coding assistant"
    echo "  ./launch_qwen.sh system_prompt_coding.txt --v4  # V4 with coding assistant"
    echo ""
    if [ "$use_v4" = true ]; then
        echo "🚀 Starting V4 with default filesystem prompt..."
    else
        echo "🚀 Starting V5 with enhanced filesystem + code analysis..."
    fi
    python "$version_script"
fi