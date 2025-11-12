import os

# Путь к папке с твоими заметками Obsidian
NOTES_FOLDER = "/Users/nurma/obsidian_sync/IT/Machine Learning"

# Тег, который нужно добавить
TAG = "#AI"

def add_tag_to_notes(folder, tag):
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.endswith(".md"):  # только markdown заметки
                file_path = os.path.join(root, filename)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                # Проверяем, есть ли уже тег
                if tag not in content:
                    new_content = content + "\n\n" + tag

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    print(f"✅ Тег добавлен: {filename}")
                else:
                    print(f"⏩ Тег уже есть: {filename}")

if __name__ == "__main__":
    add_tag_to_notes(NOTES_FOLDER, TAG)
