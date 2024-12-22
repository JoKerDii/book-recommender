import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from tools.output_parser import output_parser, Recommendations
from third_party.book_search import search_books

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

def summarize_description(description):
    if not description:
        return "No description available."
    
    prompt = """
    Summarize the following book description in 2-3 sentences:\n\n{description}"""

    prompt_template = PromptTemplate(
        input_variables=["description"],
        template=prompt,
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    chain = prompt_template | llm
    response = chain.invoke(input={"description": description})
    
    return response

def recommend_books(books):
    summary_template = """
    Based on the following list of books, suggest other similar books:
    \n{booklist}
    
    Provide a list of 3 book recommendations.
    
    Each recommendation should include the following fields:\n"
        "1. title: The title of the book (string).\n"
        "2. summary: A brief summary of the book (string).\n"
        "3. authors: A list of authors (list of strings).\n"
        "4. rating: The average rating of the book (number, float).\n"
        "5. link: A link to more information about the book (string).\n\n"
    \n{format_instructions}
    """
    book_list = ""
    for book in books:
        book_list += f"Title: {book['title']}, Authors: {', '.join(book.get('authors', []))}, Description: {book.get('description', 'No description')}\n\n"
    
    summary_prompt_template = PromptTemplate(
        input_variables=["booklist"],
        template=summary_template,
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )
    chain = summary_prompt_template | llm | output_parser
    recommendations = chain.invoke(input={"booklist": book_list})

    return recommendations

def search_and_recommend_books(query):
    print(f"Searching for books related to '{query}'...\n")
    books = search_books(query)
    
    summarized_books = []
    for book in books:
        summary = summarize_description(book.get("description"))
        summarized_books.append({
            "title": book["title"],
            "authors": book["authors"],
            "summary": summary,
            "rating": book.get("averageRating"),
            "link": book["infoLink"]
        })
    
    # print("Summarized Results:")
    # for book in summarized_books:
    #     print(f"Title: {book['title']}")
    #     print(f"Authors: {', '.join(book['authors'] or [])}")
    #     print(f"Summary: {book['summary']}")
    #     print(f"Rating: {book.get('rating', 'N/A')}")
    #     print(f"More Info: {book['link']}\n")
    
    print("Generating recommendations...")
    recommendations = recommend_books(books)
    # print("Recommended Books:")
    # print(recommendations)

    # convert to dictionary
    recommendations = recommendations.to_dict()
    recommendations_dict = {}
    for i, r in enumerate(recommendations['Recommendations']):
        recommendations_dict["Recommendation"+str(i)] = r.to_dict()
    return recommendations_dict


if __name__ == "__main__":
    query = 'work efficiency'
    out = search_and_recommend_books(query)
    print(out)
    
    