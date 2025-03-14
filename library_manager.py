import json
import streamlit as st

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        with open(self.filename, "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, title, author, year, genre, read_status):
        self.books.append({
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read_status": read_status
        })
        self.save_books()

    def remove_book(self, title):
        self.books = [book for book in self.books if book["title"].lower() != title.lower()]
        self.save_books()

    def search_books(self, keyword):
        return [book for book in self.books if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]

    def get_statistics(self):
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book["read_status"])
        percentage_read = (read_books / total_books * 100) if total_books else 0
        return total_books, read_books, percentage_read

library = Library()

st.set_page_config(page_title="Personal Library Manager", layout="wide")
st.title("📚 Personal Library Manager")

st.sidebar.header("📖 Menu")
menu_option = st.sidebar.radio("Select an option", ["Add Book", "Remove Book", "Search Book", "View All Books", "Statistics"], index=0)

st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
    }
    .stTextInput, .stNumberInput, .stButton>button {
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #ff6f61;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e65c50;
    }
    .stSidebar {
        background-color: #D3D3D3;
        padding: 20px;
        color: Black;
        border-radius: 10px;
    }
    .stMetric {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if menu_option == "Add Book":
    with st.form("add_book_form"):
        title = st.text_input("📖 Title")
        author = st.text_input("✍ Author")
        year = st.number_input("📅 Publication Year", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("📚 Genre")
        read_status = st.checkbox("✅ Have you read it?")
        submit = st.form_submit_button("➕ Add Book")
        if submit:
            library.add_book(title, author, year, genre, read_status)
            st.success("✅ Book added successfully!")

elif menu_option == "Remove Book":
    title = st.text_input("❌ Enter book title to remove")
    if st.button("🗑 Remove Book"):
        library.remove_book(title)
        st.success("🗑 Book removed successfully!")

elif menu_option == "Search Book":
    keyword = st.text_input("🔍 Enter title or author")
    if st.button("🔎 Search"):
        results = library.search_books(keyword)
        if results:
            for book in results:
                st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read_status'] else '❌ Unread'}")
        else:
            st.warning("🚫 No matching books found.")

elif menu_option == "View All Books":
    books = library.books
    if books:
        for book in books:
            st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read_status'] else '❌ Unread'}")
    else:
        st.warning("📂 No books in the library.")

elif menu_option == "Statistics":
    total_books, read_books, percentage_read = library.get_statistics()
    st.metric("📚 Total Books", total_books)
    st.metric("✅ Books Read", read_books)
    st.metric("📊 Percentage Read", f"{percentage_read:.2f}%")
