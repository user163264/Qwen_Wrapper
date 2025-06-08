#!/usr/bin/env python3
"""
Filesystem Handler for Qwen Model Function Calling
Provides secure filesystem operations within restricted directories.
"""

import os
import json
import shutil
import glob
from pathlib import Path
from typing import List, Dict, Any, Union
from datetime import datetime

class FilesystemHandler:
    def __init__(self, allowed_directories: List[str] = None):
        """
        Initialize the filesystem handler with security restrictions.
        
        Args:
            allowed_directories: List of directory paths that operations are restricted to.
                                If None, defaults to safe directories.
        """
        if allowed_directories is None:
            # Default safe directories - modify as needed
            self.allowed_directories = [
                "/Users/admin/Documents/Qwen_Coder_Local",
                "/Users/admin/Documents/test_workspace",
                "/Users/admin/Desktop/qwen_workspace"
            ]
        else:
            self.allowed_directories = allowed_directories
        
        # Normalize paths to absolute paths
        self.allowed_directories = [os.path.abspath(path) for path in self.allowed_directories]
        
        # Create allowed directories if they don't exist
        for directory in self.allowed_directories:
            os.makedirs(directory, exist_ok=True)
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if a path is within allowed directories."""
        abs_path = os.path.abspath(path)
        return any(abs_path.startswith(allowed_dir) for allowed_dir in self.allowed_directories)
    
    def _validate_path(self, path: str) -> str:
        """Validate and normalize a path."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access denied: Path '{path}' is outside allowed directories")
        return os.path.abspath(path)
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read the complete contents of a file."""
        try:
            validated_path = self._validate_path(file_path)
            
            if not os.path.exists(validated_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            if not os.path.isfile(validated_path):
                return {"success": False, "error": f"Path is not a file: {file_path}"}
            
            with open(validated_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return {
                "success": True,
                "content": content,
                "file_path": file_path,
                "size": len(content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Create a new file or overwrite an existing file."""
        try:
            validated_path = self._validate_path(file_path)
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(validated_path), exist_ok=True)
            
            with open(validated_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return {
                "success": True,
                "message": f"File written successfully: {file_path}",
                "file_path": file_path,
                "size": len(content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def append_to_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Append content to an existing file or create new file."""
        try:
            validated_path = self._validate_path(file_path)
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(validated_path), exist_ok=True)
            
            with open(validated_path, 'a', encoding='utf-8') as file:
                file.write(content)
            
            return {
                "success": True,
                "message": f"Content appended successfully: {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_directory(self, directory_path: str, include_hidden: bool = False) -> Dict[str, Any]:
        """List files and directories in a specified directory."""
        try:
            validated_path = self._validate_path(directory_path)
            
            if not os.path.exists(validated_path):
                return {"success": False, "error": f"Directory not found: {directory_path}"}
            
            if not os.path.isdir(validated_path):
                return {"success": False, "error": f"Path is not a directory: {directory_path}"}
            
            items = []
            for item in os.listdir(validated_path):
                if not include_hidden and item.startswith('.'):
                    continue
                
                item_path = os.path.join(validated_path, item)
                item_type = "directory" if os.path.isdir(item_path) else "file"
                
                items.append({
                    "name": item,
                    "type": item_type,
                    "path": item_path
                })
            
            return {
                "success": True,
                "directory_path": directory_path,
                "items": items,
                "count": len(items)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_directory(self, directory_path: str) -> Dict[str, Any]:
        """Create a new directory."""
        try:
            validated_path = self._validate_path(directory_path)
            
            os.makedirs(validated_path, exist_ok=True)
            
            return {
                "success": True,
                "message": f"Directory created successfully: {directory_path}",
                "directory_path": directory_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete a specific file."""
        try:
            validated_path = self._validate_path(file_path)
            
            if not os.path.exists(validated_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            if not os.path.isfile(validated_path):
                return {"success": False, "error": f"Path is not a file: {file_path}"}
            
            os.remove(validated_path)
            
            return {
                "success": True,
                "message": f"File deleted successfully: {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_directory(self, directory_path: str, force: bool = False) -> Dict[str, Any]:
        """Delete a directory and all its contents."""
        try:
            validated_path = self._validate_path(directory_path)
            
            if not os.path.exists(validated_path):
                return {"success": False, "error": f"Directory not found: {directory_path}"}
            
            if not os.path.isdir(validated_path):
                return {"success": False, "error": f"Path is not a directory: {directory_path}"}
            
            if not force and os.listdir(validated_path):
                return {"success": False, "error": f"Directory not empty: {directory_path}. Use force=True to delete."}
            
            shutil.rmtree(validated_path)
            
            return {
                "success": True,
                "message": f"Directory deleted successfully: {directory_path}",
                "directory_path": directory_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_files(self, search_path: str, pattern: str, recursive: bool = True) -> Dict[str, Any]:
        """Search for files matching a pattern."""
        try:
            validated_path = self._validate_path(search_path)
            
            if not os.path.exists(validated_path):
                return {"success": False, "error": f"Search path not found: {search_path}"}
            
            if not os.path.isdir(validated_path):
                return {"success": False, "error": f"Search path is not a directory: {search_path}"}
            
            matches = []
            if recursive:
                search_pattern = os.path.join(validated_path, "**", pattern)
                matches = glob.glob(search_pattern, recursive=True)
            else:
                search_pattern = os.path.join(validated_path, pattern)
                matches = glob.glob(search_pattern)
            
            # Filter to only include allowed paths
            allowed_matches = [match for match in matches if self._is_path_allowed(match)]
            
            results = []
            for match in allowed_matches:
                item_type = "directory" if os.path.isdir(match) else "file"
                results.append({
                    "path": match,
                    "name": os.path.basename(match),
                    "type": item_type
                })
            
            return {
                "success": True,
                "search_path": search_path,
                "pattern": pattern,
                "matches": results,
                "count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """Get detailed information about a file or directory."""
        try:
            validated_path = self._validate_path(path)
            
            if not os.path.exists(validated_path):
                return {"success": False, "error": f"Path not found: {path}"}
            
            stat = os.stat(validated_path)
            
            info = {
                "success": True,
                "path": path,
                "name": os.path.basename(validated_path),
                "type": "directory" if os.path.isdir(validated_path) else "file",
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:]
            }
            
            if os.path.isfile(validated_path):
                info["extension"] = os.path.splitext(validated_path)[1]
            
            return info
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def move_file(self, source_path: str, destination_path: str) -> Dict[str, Any]:
        """Move or rename a file."""
        try:
            validated_source = self._validate_path(source_path)
            validated_dest = self._validate_path(destination_path)
            
            if not os.path.exists(validated_source):
                return {"success": False, "error": f"Source file not found: {source_path}"}
            
            if os.path.exists(validated_dest):
                return {"success": False, "error": f"Destination already exists: {destination_path}"}
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(validated_dest), exist_ok=True)
            
            shutil.move(validated_source, validated_dest)
            
            return {
                "success": True,
                "message": f"File moved successfully: {source_path} -> {destination_path}",
                "source_path": source_path,
                "destination_path": destination_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def copy_file(self, source_path: str, destination_path: str) -> Dict[str, Any]:
        """Copy a file to another location."""
        try:
            validated_source = self._validate_path(source_path)
            validated_dest = self._validate_path(destination_path)
            
            if not os.path.exists(validated_source):
                return {"success": False, "error": f"Source file not found: {source_path}"}
            
            if not os.path.isfile(validated_source):
                return {"success": False, "error": f"Source is not a file: {source_path}"}
            
            if os.path.exists(validated_dest):
                return {"success": False, "error": f"Destination already exists: {destination_path}"}
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(validated_dest), exist_ok=True)
            
            shutil.copy2(validated_source, validated_dest)
            
            return {
                "success": True,
                "message": f"File copied successfully: {source_path} -> {destination_path}",
                "source_path": source_path,
                "destination_path": destination_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_allowed_directories(self) -> Dict[str, Any]:
        """Get the list of allowed directories."""
        return {
            "success": True,
            "allowed_directories": self.allowed_directories,
            "count": len(self.allowed_directories)
        }


# Function dispatcher for LMStudio function calling
def handle_function_call(function_name: str, arguments: Dict[str, Any]) -> str:
    """
    Handle function calls from LMStudio and return JSON response.
    
    Args:
        function_name: Name of the function to call
        arguments: Dictionary of function arguments
    
    Returns:
        JSON string with the function result
    """
    # Initialize handler (modify allowed directories as needed)
    handler = FilesystemHandler()
    
    # Map function names to handler methods
    function_map = {
        "read_file": handler.read_file,
        "write_file": handler.write_file,
        "append_to_file": handler.append_to_file,
        "list_directory": handler.list_directory,
        "create_directory": handler.create_directory,
        "delete_file": handler.delete_file,
        "delete_directory": handler.delete_directory,
        "search_files": handler.search_files,
        "get_file_info": handler.get_file_info,
        "move_file": handler.move_file,
        "copy_file": handler.copy_file,
        "get_allowed_directories": handler.get_allowed_directories
    }
    
    if function_name not in function_map:
        return json.dumps({
            "success": False,
            "error": f"Unknown function: {function_name}"
        })
    
    try:
        # Call the appropriate function with the provided arguments
        result = function_map[function_name](**arguments)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Function call failed: {str(e)}"
        })


if __name__ == "__main__":
    # Test the handler
    handler = FilesystemHandler()
    
    # Test creating a directory
    result = handler.create_directory("/Users/admin/Documents/Qwen_Coder_Local/test")
    print("Create directory result:", json.dumps(result, indent=2))
    
    # Test writing a file
    result = handler.write_file("/Users/admin/Documents/Qwen_Coder_Local/test/hello.txt", "Hello, Qwen!")
    print("Write file result:", json.dumps(result, indent=2))
    
    # Test reading the file
    result = handler.read_file("/Users/admin/Documents/Qwen_Coder_Local/test/hello.txt")
    print("Read file result:", json.dumps(result, indent=2))
    
    # Test listing directory
    result = handler.list_directory("/Users/admin/Documents/Qwen_Coder_Local/test")
    print("List directory result:", json.dumps(result, indent=2))
