import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil

class AppPublisher:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline App Publisher")

        tk.Label(root, text="App Name").pack()
        self.app_name_entry = tk.Entry(root, width=50)
        self.app_name_entry.pack()

        tk.Label(root, text="Python File").pack()
        self.py_entry = tk.Entry(root, width=50)
        self.py_entry.pack()
        tk.Button(root, text="Browse", command=self.browse_py).pack()

        tk.Label(root, text="Icon File (Optional)").pack()
        self.icon_entry = tk.Entry(root, width=50)
        self.icon_entry.pack()
        tk.Button(root, text="Browse Icon", command=self.browse_icon).pack()

        tk.Label(root, text="Additional Zipped Files (Optional)").pack()
        self.zip_entry = tk.Entry(root, width=50)
        self.zip_entry.pack()
        tk.Button(root, text="Browse Zip", command=self.browse_zip).pack()

        tk.Button(root, text="Build App", command=self.build_app, bg="green", fg="white").pack(pady=10)

    def browse_py(self):
        file = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        self.py_entry.delete(0, tk.END)
        self.py_entry.insert(0, file)

    def browse_icon(self):
        file = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        self.icon_entry.delete(0, tk.END)
        self.icon_entry.insert(0, file)

    def browse_zip(self):
        file = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        self.zip_entry.delete(0, tk.END)
        self.zip_entry.insert(0, file)

    def build_app(self):
        py_file = self.py_entry.get()
        icon_path = self.icon_entry.get()
        zip_file = self.zip_entry.get()
        app_name = self.app_name_entry.get() or "MyApp"

        if not py_file or not os.path.exists(py_file):
            messagebox.showerror("Error", "Python file not selected or invalid.")
            return

        output_dir = os.path.join(os.path.dirname(py_file), "dist")

        # If there's a zip file, extract it to the same dir as the Python file
        if zip_file and os.path.exists(zip_file):
            try:
                shutil.unpack_archive(zip_file, os.path.dirname(py_file))
            except Exception as e:
                messagebox.showerror("Zip Error", f"Failed to unpack zip file: {e}")
                return

        # Build command for PyInstaller
        command = [
            "pyinstaller",
            "--noconfirm",
            "--onefile",
            "--distpath", output_dir,
            "--name", app_name,
        ]

        if icon_path and os.path.exists(icon_path):
            command += ["--icon", icon_path]

        command.append(py_file)

        try:
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Success", f"App built successfully in: {output_dir}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Build Failed", f"Failed to compile the Python file.\n\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPublisher(root)
    root.mainloop()
