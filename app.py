import streamlit as st
from model import Model

# UI using Streamlit
st.subheader("Business Idea Generator 📝")
st.text("Generates Taglines, Web Domains, Marketing strategies:List of marketing strategies and Competitors")

categories: tuple = ("Food & Beverage",
    "Clothing & Apparals",
    "Healthcare & Fitness", 
    "Education",
    "Social Impact",
    "Environmental Impact",
    "Technology & Hardware",
    "Others"
)

category: str = st.sidebar.selectbox("Pick a Business Category", categories)
idea: str = st.text_input(label="Enter a Business Idea", placeholder="Ex: Airlines Company", max_chars=200)
display_items: list[str] = ["Brand Name", "📌 Taglines", "🌐 Web Domains", "💸 Marketing Strategies", "📍 Competitors"]

# Instantiate the model
model = Model()

# Handling content generation
def handlePress():
    if category and idea != "":
        st.balloons()
        result, business_name = model.generate_content(category = category, idea = idea)
        st.header("# " + business_name.name)

        st.subheader("📌 Taglines")
        for tagline in result.taglines:
            st.write("- " + tagline)

        st.subheader("🌐 Web Domains")
        for domain in result.domains:
            st.write("- " + domain)

        st.subheader("💸 Marketing Strategies")
        for strategy in result.strats:
            st.write("- " + strategy)

        st.subheader("📍 Competitors")
        for competitor in result.comp:
            st.write("- " + competitor)
        
    elif idea == "":
        for item in display_items:
            st.subheader(item)
            st.write("- Generates " + item.lower().split(" ")[-1])
    else:
        pass

st.button(label="Generate content", on_click=handlePress())
 