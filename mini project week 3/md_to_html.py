import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re
import html

class MarkdownConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MD to HTML Converter")
        self.root.geometry("400x200")
        
        self.converter = MarkdownConverter()
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        ttk.Label(main_frame, text="Select Markdown File:").grid(row=0, column=0, sticky=tk.W)
        self.file_entry = ttk.Entry(main_frame, width=35)
        self.file_entry.grid(row=1, column=0, padx=5, pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=1, column=1, padx=5)
        
        # Convert button
        convert_btn = ttk.Button(main_frame, text="Convert to HTML", command=self.convert_file)
        convert_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="red")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.status_label.config(text="")
            
    def convert_file(self):
        input_path = self.file_entry.get()
        if not input_path:
            self.status_label.config(text="Please select a Markdown file!")
            return
            
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_body = self.converter.convert(md_content)
            output_file = os.path.splitext(input_path)[0] + '.html'
            title = os.path.basename(input_path)
            
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
</head>
<body>
{html_body}
</body>
</html>"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            #self.status_label.config(text=f"Converted: {output_file}", foreground="green")
            messagebox.showinfo("Success", "File converted successfully!")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", str(e))

class MarkdownConverter:
    def __init__(self):
        self.rules = [
            (r'# (.+)', self._header),  # Unified header handler
            (r'\*\*(.+?)\*\*', lambda m: f'<strong>{m.group(1)}</strong>'),
            (r'\*(.+?)\*', lambda m: f'<em>{m.group(1)}</em>'),
            (r'!\[(.*?)\]\((.*?)\)', lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">'),
            (r'\[(.*?)\]\((.*?)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>'),
            (r'`(.+?)`', lambda m: f'<code>{m.group(1)}</code>'),
            (r'---', '<hr>'),
            (r'[\n\r]-\s+(.+)', self._list_item),
            (r'[\n\r]\d+\.\s+(.+)', self._ordered_list_item),
        ]
        
    def _header(self, match):
        level = min(match.group(0).count('#'), 6)
        return f'<h{level}>{match.group(1)}</h{level}>'
    
    def _list_item(self, match):
        return f'<ul>\n<li>{match.group(1)}</li>\n</ul>'  # Simplified list handling
    
    def _ordered_list_item(self, match):
        return f'<ol>\n<li>{match.group(1)}</li>\n</ol>'
    
    def convert(self, md_text):
        html_content = []
        for line in md_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            for pattern, replacement in self.rules:
                if callable(replacement):
                    line = re.sub(pattern, replacement, line)
                else:
                    line = re.sub(pattern, replacement, line)
            html_content.append(line)
        return '\n'.join(html_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownConverterApp(root)
    root.mainloop()
