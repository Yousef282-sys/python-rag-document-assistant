def generate_answer(question: str, context: str) -> str:
    """
    Return a clean answer directly from the retrieved documentation.
    This avoids exposing LLM reasoning in the final response.
    """

    if not context.strip():
        return "I couldn't find enough information in the provided Python documentation."

    sections = context.split("\n\n---\n\n")

    first_section = sections[0].strip()

    lines = first_section.splitlines()

    answer_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("[Source:"):
            continue

        if line.startswith("Section:"):
            continue

        if line == "CODE:":
            continue

        answer_lines.append(line)

    answer = " ".join(answer_lines).strip()

    if len(answer) > 700:
        answer = answer[:700].rsplit(" ", 1)[0] + "."

    return answer