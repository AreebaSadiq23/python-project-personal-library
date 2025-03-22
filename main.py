import streamlit as st
import json

# File to store library data
LIBRARY_FILE = "library.json"

# Load library data from file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library data to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
db = load_library()

st.title("📚 Personal Library Manager")

# Sidebar Menu with Icons
menu = {
    "📖 Add Book": "Add Book",
    "❌ Remove Book": "Remove Book",
    "🔎 Search Book": "Search Book",
    "📚 Display All Books": "Display All Books",
    "📊 Statistics": "Statistics"
}
choice = st.sidebar.selectbox("Select an option", list(menu.keys()))

if menu[choice] == "Add Book":
    st.subheader("📖 Add a New Book")
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("📖Book Title")
        author = st.text_input("✍ Author")
    with col2:
        year = st.number_input("📅 Publication Year", min_value=0, format="%d")
        genre = st.selectbox("📚 Genre", ["Fiction", "Non-Fiction", "Mystery", "Sci-Fi", "Fantasy", "Biography", "History", "Other"])
    
    read_status = st.checkbox("Read")
    
    if st.button("➕ Add Book", use_container_width=True):
        new_book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
        db.append(new_book)
        save_library(db)
        st.success(f'✅ Book "{title}" added successfully!')

elif menu[choice] == "Remove Book":
    st.subheader("❌ Remove a Book")
    book_titles = [book["title"] for book in db]
    book_to_remove = st.selectbox("Select a book to remove", book_titles)
    
    if st.button("🗑 Remove Book", use_container_width=True):
        db = [book for book in db if book["title"] != book_to_remove]
        save_library(db)
        st.success(f'❌ Book "{book_to_remove}" removed successfully!')

elif menu[choice] == "Search Book":
    st.subheader("🔎 Search for a Book")
    search_term = st.text_input("Enter book title or author")
    
    if st.button("🔍 Search", use_container_width=True):
        results = [book for book in db if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.markdown(f'📖 **{book["title"]}** by *{book["author"]}* ({book["year"]}) - {book["genre"]} | Read: {"✔" if book["read"] else "❌"}')
        else:
            st.warning("⚠ No books found.")

elif menu[choice] == "Display All Books":
    st.subheader("📚 Library Collection")
    if db:
        for book in db:
            st.markdown(f'📘 **{book["title"]}** by *{book["author"]}* ({book["year"]}) - {book["genre"]} | Read: {"✔" if book["read"] else "❌"}')
    else:
        st.warning("⚠ No books in the library.")

elif menu[choice] == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(db)
    read_books = sum(1 for book in db if book["read"])
    unread_books = total_books - read_books
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.metric("📚 Total Books", total_books)
    st.metric("📖 Read Books", read_books)
    st.metric("📕 Unread Books", unread_books)
    
    st.progress(percentage_read / 100)
    st.write(f'📊 **{percentage_read:.2f}%** of books read.')
