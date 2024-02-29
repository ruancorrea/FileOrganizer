import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import locale
import time

class FileOrganizer:
    def __init__(self, entry_path, language) -> None:
        self.extensions_for_folders_application = self.extensions_for_folders_dict()
        self.path_folder_application = self.get_downloads_folder()
        self.extensions_available_GUI = []
        self.entry_path = entry_path
        self.checkboxes = []
        self.language = language

    def get_downloads_folder(self):
        # Verificar o sistema operacional
        if os.name == 'nt':  # Windows
            downloads_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        elif os.name == 'posix':  # Linux ou macOS
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            # Sistema operacional não suportado
            downloads_folder = None
        return downloads_folder
    
    def extensions_for_folders_dict(self):
        # Mapeamento de extensões para pastas
        system_lang, _ = locale.getdefaultlocale()
        if system_lang.startswith('pt'):
            return {
                '.jpg': 'imagens', '.jpeg': 'imagens', '.png': 'imagens', '.gif': 'imagens', '.webp': 'imagens', '.svg': 'imagens', '.jfif': 'imagens',
                '.mp4': 'videos', '.avi': 'videos', '.mkv': 'videos',
                '.mp3': 'musicas',
                '.psd': 'photoshop',
                '.zip': 'arquivos_compactados', '.rar': 'arquivos_compactados',
                '.exe': 'programas', '.msi': 'programas',
                '.pdf': 'pdfs',
                '.txt': 'txt',
                '.docx': 'docs', '.doc': 'docs', '.xlsx': 'docs', '.xls': 'docs', '.xlsm': 'docs', '.csv': 'docs', '.pptx': 'docs',
                '.json': 'json',
                '.html': 'html', '.xml': 'hmtl',
            }
        else:
            return {
                '.jpg': 'images', '.jpeg': 'images', '.png': 'images', '.gif': 'images', '.webp': 'images', '.svg': 'images', '.jfif': 'images',
                '.mp4': 'videos', '.avi': 'videos', '.mkv': 'videos',
                '.mp3': 'songs',
                '.psd': 'photoshop',
                '.zip': 'compressed_files', '.rar': 'compressed_files',
                '.exe': 'software', '.msi': 'software',
                '.pdf': 'pdfs',
                '.txt': 'txt',
                '.docx': 'docs', '.doc': 'docs', '.xlsx': 'docs', '.xls': 'docs', '.xlsm': 'docs', '.csv': 'docs', '.pptx': 'docs',
                '.json': 'json',
                '.html': 'html', '.xml': 'hmtl',
            }
        
    def wait_in_seconds(self, duration_in_seconds):
        init_time = time.time()
        while True:
            current_time = time.time()
            difference_time = current_time - init_time
            if difference_time >= duration_in_seconds:
                break
        
    def extensions_for_folders_format_GUI(self):
        return [f"{k} ({v})" for k,v in self.extensions_for_folders_application.items()]

    def select_folder(self):
        path = filedialog.askdirectory()
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, path)

    def select_all_extensions(self):
        for var in self.checkboxes:
            var.set(1)

    def unmark_all_extensions(self):
        for var in self.checkboxes:
            var.set(0)

    def extensions_for_folders(self, selected_extensions):
        # Certifique-se de que as pastas de destino existem
        for destination_folder in self.extensions_for_folders_application.values():
            folder = os.path.join(self.path_folder_application, destination_folder)
            if not os.path.exists(folder):
                os.makedirs(folder)

        # Iterar pelos arquivos na pasta de downloads
        for file in os.listdir(self.path_folder_application,):
            file_path = os.path.join(self.path_folder_application, file)
            if os.path.isfile(file_path):            # Verificar se é um arquivo
                _, extension = os.path.splitext(file.lower())                # Obter a extensão do arquivo

                # Verificar se a extensão está na lista de extensões selecionadas
                if extension in selected_extensions and extension in self.extensions_for_folders_application:
                    destination_folder = self.extensions_for_folders_application[extension]
                    destination_path = os.path.join(self.path_folder_application, destination_folder, extension)
                    shutil.move(file_path, destination_path)

    def start_process(self):
        self.path_folder_application = self.entry_path.get()
        if not self.path_folder_application:
            messagebox.showerror(self.language["error"], self.language["select_folder"])
            return
        selected_extensions = [self.extensions_available_GUI[i].split(' (')[0] for i, extension in enumerate(self.checkboxes) if extension.get()]
        if not selected_extensions:
            messagebox.showerror(self.language["error"], self.language["select_extensions"])
            return
        self.extensions_for_folders(selected_extensions)
        self.wait_in_seconds(3)
        messagebox.showinfo(self.language["info"], self.language["process_completed"])
        


def get_language():
    system_lang, _ = locale.getdefaultlocale()
    if system_lang.startswith('pt'):
        language = {
            "file_organizer": "Organizador de Arquivos",
            "error": "Erro",
            "select_folder": "Selecionar Pasta",
            "select_extensions": "Por favor, selecione pelo menos uma extensão:",
            "info": "Concluído",
            "process_completed": "O processo foi concluído com sucesso.",
            "folder_path": "Caminho da Pasta:",
            "select_all": "Selecione Todas",
            "unmark_all": "Desmarque Todas",
            "start_process": "Iniciar Processo",
        }
    else:
        language = {
            "file_organizer": "File Organizer",
            "error": "Error",
            "select_folder": "Folder path.",
            "select_extensions": "Please select at least one extension.",
            "info": "Info",
            "process_completed": "The process has been completed successfully.",
            "folder_path": "Folder path:",
            "select_all": "Select All",
            "unmark_all": "Unmark All",
            "start_process": "Start Process",
        }
    return language

def GUI_application_construction(language):

    root = tk.Tk()
    root.title(language["file_organizer"])
    root.geometry("775x415")  # Definir tamanho fixo da janela
    root.resizable(False, False)  # Impedir que a janela seja redimensionada

    # Criar e posicionar os widgets na janela
    label_path = tk.Label(root, text=language["folder_path"])
    label_path.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entry_path = tk.Entry(root, width=50)
    entry_path.grid(row=0, column=1, padx=5, pady=5)
    file_organizer = FileOrganizer(entry_path=entry_path, language=language)
    entry_path.insert(0, file_organizer.get_downloads_folder() if file_organizer.get_downloads_folder() else '')
    file_organizer.entry_path=entry_path

    button_select_path = tk.Button(root, text=language["select_folder"], command=file_organizer.select_folder)
    button_select_path.grid(row=0, column=2, padx=5, pady=5)

    label_extensions = tk.Label(root, text=language["select_extensions"])
    label_extensions.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

    n = 4
    file_organizer.extensions_for_folders_application = file_organizer.extensions_for_folders_dict()
    file_organizer.extensions_available_GUI =  file_organizer.extensions_for_folders_format_GUI()

    for i, ext in enumerate(file_organizer.extensions_available_GUI ):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(root, text=ext, variable=var, onvalue=1, offvalue=0)
        checkbox.grid(row=i // n + 2, column=i % n, padx=n, pady=n, sticky="w")
        file_organizer.checkboxes.append(var)

    button_select_all = tk.Button(root, text=language["select_all"], command=file_organizer.select_all_extensions)
    button_select_all.grid(row=(len(file_organizer.extensions_available_GUI ) // n) + 2, column=3, columnspan=n, padx=2, pady=2)
    button_unmark_all = tk.Button(root, text=language["unmark_all"], command=file_organizer.unmark_all_extensions)
    button_unmark_all.grid(row=(len(file_organizer.extensions_available_GUI ) // n) + 3, column=3, columnspan=n, padx=2, pady=2)

    button_start = tk.Button(root, text=language["start_process"], command=file_organizer.start_process)
    button_start.grid(row=(len(file_organizer.extensions_available_GUI ) // n) + 4, columnspan=n, padx=5, pady=10)

    return root


if __name__ == '__main__':
    language = get_language()
    root = GUI_application_construction(language)
    root.mainloop()
