
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

llm = ChatOllama(model="llama3.1:8b", temperature=0, format="json")

def main():

    class Entities(BaseModel):
        """Identifying information about entities."""

        names: list[str] = Field(
            ...,
            description="All the codes, regulations, standards entities that appear in the text",
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are extracting organization and person entities from the text.",
            ),
            (
                "human",
                "Use the given format to extract information from the following "
                "input: {question}",
            ),
        ]
    )


    entity_chain = llm.with_structured_output(Entities)

    return entity_chain, prompt
