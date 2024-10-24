import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Simvolların siyahısı
ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Piksel rəngini simvollara çevirmə funksiyası
def pixel_to_ascii(pixel):
    r, g, b = pixel[:3]
    gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)  # Boz səviyyə
    return ascii_chars[gray * len(ascii_chars) // 256], f'#{r:02x}{g:02x}{b:02x}'  # Simvol və rəng kodu qaytarılır

# Şəkili oxuyan və simvollara çevirən funksiya
def convert_image_to_ascii(image, max_width_in_chars):
    width, height = image.size
    aspect_ratio = height / width

    # Yeni ölçüləri müəyyən etmək (şəkilin genişliyini max_width'ə uyğun olaraq dəyişirik)
    new_width = max_width_in_chars  # ASCII-nin eninə uyğun
    new_height = int(aspect_ratio * new_width * 0.55)  # Hündürlük, ASCII-nin hündürlük nisbətinə uyğun olaraq
    image = image.resize((new_width, new_height))

    ascii_data = []
    for y in range(image.height):
        line_data = []
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            ascii_char, color = pixel_to_ascii(pixel)
            line_data.append((ascii_char, color))
        ascii_data.append(line_data)
    
    return ascii_data

# Render prosesini simvol-simvol göstərmək
def display_ascii_data(ascii_data, text_widget, delay=5):
    total_lines = len(ascii_data)
    total_time = delay  # 5 saniyəlik limit daxilində bitməlidir
    time_per_line = total_time / total_lines

    def write_line(line_index):
        if line_index >= total_lines:
            return
        
        line_data = ascii_data[line_index]
        for x, (ascii_char, color) in enumerate(line_data):
            tag_name = f"color_{line_index}_{x}"  # Hər simvol üçün unikal tag adı
            text_widget.tag_configure(tag_name, foreground=color)
            text_widget.insert(tk.END, ascii_char, tag_name)
        text_widget.insert(tk.END, "\n")
        text_widget.update_idletasks()

        # Növbəti sətiri təyin olunmuş gecikmə ilə göstər
        text_widget.after(int(time_per_line * 1000), write_line, line_index + 1)

    write_line(0)

# Loqo şəkilini açan və vizuallaşdıran funksiya
def visualize_logo():
    logo_path = "./img/BDU.png"  # Loqo faylının ünvanını burada yazın
    img = Image.open(logo_path)
    ascii_area.delete(1.0, tk.END)  # ASCII sahəsini təmizləyək
    max_width_in_chars = ascii_area.winfo_width() // 6  # Hər simvolun təxmini eni (Courier fontu üçün)
    ascii_data = convert_image_to_ascii(img, max_width_in_chars)
    display_ascii_data(ascii_data, ascii_area, delay=5)  # 5 saniyəlik limit daxilində bitəcək

# Şəkil seçən funksiya
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        ascii_area.delete(1.0, tk.END)  # ASCII sahəsini təmizləyək
        max_width_in_chars = ascii_area.winfo_width() // 6  # Hər simvolun təxmini eni (Courier fontu üçün)
        ascii_data = convert_image_to_ascii(img, max_width_in_chars)
        display_ascii_data(ascii_data, ascii_area, delay=5)  # Yeni şəkil 5 saniyə ərzində göstəriləcək

# Tkinter interfeysini qurmaq
root = tk.Tk()
root.title("BDU Tətbiqi Riyaziyyat və Kibernetika")

# Pəncərə ölçüsünü təyin edək
root.geometry("800x600")

# Üst çərçivə (Header)
header_frame = tk.Frame(root)
header_frame.pack(side=tk.TOP, fill=tk.X)

# Loqo üçün şəkili yükləmək
logo_path = "./img/BDU.png"  # Loqo faylının ünvanını burada yazın
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((50, 50))  # Loqonun ölçüsünü dəyişmək
logo_photo = ImageTk.PhotoImage(logo_image)

# Loqo (Label)
logo_label = tk.Label(header_frame, image=logo_photo)
logo_label.pack(side=tk.LEFT, padx=10, pady=10)

# Mətn və düymə (Header hissədə)
header_label = tk.Label(header_frame, text="BDU TƏTBİQİ RİYAZİYYAT VƏ KİBERNETİKA", font=("Arial", 16), padx=10, pady=10)
header_label.pack(side=tk.LEFT)

# Şəkil seç düyməsi və sağ tərəfdən boşluq (padx)
select_button = tk.Button(header_frame, text="Şəkil seç", command=select_image, padx=10, pady=5)
select_button.pack(side=tk.RIGHT, padx=20)

# Aşağı çərçivə (ASCII vizuallaşma hissəsi)
ascii_frame = tk.Frame(root)
ascii_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# ASCII mətn sahəsi
ascii_area = tk.Text(ascii_frame, font=("Courier", 6), bg="black", fg="white")
ascii_area.pack(expand=True, fill=tk.BOTH)

# Proqram açılan kimi loqo şəkilini vizuallaşdıraq
root.after(100, visualize_logo)

root.mainloop()
