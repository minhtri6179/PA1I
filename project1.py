import time
# IO file
def read_file(filename):
    data_dict = {}
    with open(filename, "r") as file_in:
        data = file_in.readline()
        left_side = data.split("=")[0]
        right_side = data.split("=")[-1]
        # save data to dict
        data_dict["LHS"], data_dict["LHSvsOperator"] = split_words_operator(left_side)
        data_dict["RHS"] = right_side
    return data_dict
def write_file(filename, result):
    with open(filename, "a") as file_in:
        file_in.write(f"{result}\n")
    return True
def split_words_operator(str):
    """ Split a string to list of words and list of operators and words

    Args:
        str ([type])

    Returns:
        [list]: [list of words after split]
        [list]: [list of words and operator after split]
    """
    words = []
    words_operator = []
    temp = ""
    for i in range(len(str)):
        if (str[i] != "+" and str[i] != "-" and str[i] != "*"
                and str[i] != "(" and str[i] != ")"):
            temp += str[i]
        else:
            if temp != "":
                words.append(temp)
                words_operator.append(temp)
            words_operator.append(str[i])
            temp = ""
    words.append(temp)
    words_operator.append(temp)
    return words, words_operator
# IO file

def get_variables(left_right_side):
    variables = []
    for word in left_right_side["LHS"]:
        variables += list(word)
    variables += list(left_right_side["RHS"])
    # return list of distinct variables
    return list(set(variables))
def get_valid_digit(data, letters):
    valid_digit = {}
    # Digits is from 0-9
    for letter in letters:
        valid_digit[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    max_length_word = len(data["LHS"][0])
    for word in data["LHS"]:
        # first value on the left each word must not be 0
        valid_digit[word[0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if max_length_word < len(word):
            max_length_word = len(word)
    if len(data["RHS"]) > max_length_word:
        # first value on the right hand side must be 1
        valid_digit[str(list(data["RHS"])[0])] = [1]
    else:
        # first letter must not be 0
        valid_digit[str(list(data["RHS"])[0])] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return valid_digit

def is_satisfied(data, assignedVariables, variables):
    # eliminate duplicate
    if len(set(assignedVariables.values())) < len(assignedVariables):
        return False
    # check satisfied
    if len(assignedVariables) == len(variables):
        unit = 1
        lhsNumbers = []
        tmpNumber = 0
        tmpWord = ""
        assignedWords = {}
        for index in range(len(data["LHS"])):
            for letter in reversed(data["LHS"][index]):
                tmpNumber += assignedVariables[letter] * unit
                tmpWord += letter
                unit = unit * 10
            lhsNumbers.append(tmpNumber)
            assignedWords[tmpWord[::-1]] = tmpNumber
            tmpNumber = 0
            tmpWord = ""
            unit = 1
        rhsNumber = 0
        unit = 1
        for letter in reversed(data["RHS"]):
            rhsNumber += assignedVariables[letter] * unit
            unit = unit * 10
        expression = data["LHSvsOperator"].copy()
        for word in assignedWords.keys():
            foundIndexes = [index for index, w in enumerate(expression) if word == w]
            for i in foundIndexes:
                expression[i] = str(assignedWords[word])
        lhsResult = eval("".join(expression))
        return lhsResult == rhsNumber
    return True


def backtrack(tracking_result, variables, domains, data):
    # return if tracking_result complete
    if len(tracking_result) == len(variables):
        return tracking_result
    # variable should be assigned next
    unassigned_variables = [v for v in variables if v not in tracking_result]
    for value in domains[unassigned_variables[0]]:
        # only edit copy
        uncompleted_result = tracking_result.copy()
        uncompleted_result[unassigned_variables[0]] = value
        if is_satisfied(data, uncompleted_result, variables):
            result = backtrack(uncompleted_result, variables, domains, data)
            if result is not None:
                return result
    return None


# finally convert result to alphabet order
def to_alphabet_order(result):
    if result == None:
        return "NO SOLUTION"
    alphabet_order = sorted(result.keys())
    letter_result = {}
    for letter in alphabet_order:
        letter_result[letter] = result[letter]
    result = "".join([str(v) for v in letter_result.values()])
    return result


def cryptarithmetic(file_in):
    """
    Args:
        file_in:
    Returns:
        Write result to output.txt
    """
    data = read_file(file_in)
    variables = get_variables(data)
    domains = get_valid_digit(data, variables)
    if len(variables) > 10:
        write_file("output.txt", "NO SOLUTION")
    tracking_result = {}
    result = to_alphabet_order(backtrack(tracking_result, variables, domains, data))
    write_file("output.txt", result)

def auto_test_time():
    for i in range(4):
        for j in range(5):
            file_in = f"level{i+1}_{j+1}.txt"
            start = time.time()
            cryptarithmetic(file_in)
            end = time.time()
            with open("test.txt", 'a') as myfile:
                myfile.write(f"{end-start}\n")
            

if __name__ == '__main__':
    # auto_test_time()
    file_in = input("Which file do you want to run? (levelx_y.txt)\nType x_y: ")
    file_in = f"level{file_in}.txt"
    start = time.time()
    cryptarithmetic(file_in)
    end = time.time()
    print(f"Execution time :{end-start}")
