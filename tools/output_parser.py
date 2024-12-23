from typing import List, Optional, Any, Dict
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class BookRecommendation(BaseModel):
    title: str
    summary: str
    authors: Optional[List[str]] = None
    rating: Optional[float] = None
    link: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "authors": self.authors,
            "rating": self.rating,
            "summary": self.summary,
            "link": self.link,
        }


class Recommendations(BaseModel):
    recommendations: List[BookRecommendation]

    def to_dict(self) -> Dict[str, Any]:
        return {"Recommendations": self.recommendations}


output_parser = PydanticOutputParser(pydantic_object=Recommendations)
