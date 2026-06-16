from pathlib import Path


def contains_diff(original_text: str, modified_text: str) -> int:
    """
    Finds the closest string to the `original_text`
    inside the longer `modified_text`

    :returns: the number of characters different between the found closest string and `original_text`


    For performance reasons only evaluates the substrings offset by 0 up to 2 * len(original_text)
    from the start of the `modified_text`
    =>
    If the `modified_text` was a long enough filler + `original_text`
    the resulting difference would not be 0
    """
    if len(modified_text) < len(original_text):
        return len(original_text)

    possible_offsets: int = len(modified_text) - len(original_text) + 1
    if possible_offsets > 3 * len(original_text):
        possible_offsets = 2 * len(original_text)

    differences: list[int] = [0 for _ in range(possible_offsets)]
    for idx, char in enumerate(modified_text):
        for offset in range(max(0, idx - len(original_text) + 1), min(possible_offsets, idx + 1)):
            if char != original_text[idx - offset]:
                differences[offset] += 1


    return min(differences)


def dir_diff(input_directory: Path, original_text: str):
    diffs = []
    for item in input_directory.iterdir():
        if not item.name.endswith(".txt"):
            continue

        modified_text = item.read_text(errors='replace')

        diffs.append(contains_diff(original_text, modified_text))

    if len(diffs) == 0:
        return -1

    return sum(diffs) / len(diffs)


def diff_main(evaluated_dir: Path, original: str, replacement: str) -> None:
    result = ""
    for category in evaluated_dir.iterdir():
        print("==========================================================================")
        print("==========================================================================")
        print(f"Category: {category.name}")

        for subcategory in category.iterdir():
            print("----------------------------------------------------------------------")
            print(f"Subcategory: {subcategory.name}")

            diff = dir_diff(subcategory, original)
            result += f"{diff}\t"
            print(f"On average missing {diff} characters of original text")

            if subcategory.name == "rehidden" or subcategory.name == "rehide":
                replacement_diff = dir_diff(subcategory, replacement)
                result += f"{replacement_diff}\t"
                print(f"On average missing {replacement_diff} characters of replacement text")
        result = result.rstrip("\t")
        result += "\n"

    print("Excel result:")
    result = result.replace(".", ",")
    print(result)