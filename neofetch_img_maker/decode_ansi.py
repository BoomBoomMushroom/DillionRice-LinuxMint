def decode_ansi_file(file_path):
    try:
        # Open the ANSI text file with Windows-1252 encoding (common for ANSI files)
        with open(file_path, 'r', encoding='windows-1252') as file:
            content = file.read()
        
        # Iterate through each character in the content
        result = ""
        for char in content:
            # Get the ANSI byte value (decimal representation of the character)
            ansi_value = ord(char)  # Get the byte value of the character (0-255)
            ansiPrefix = "${c"+ str(ansi_value) +"}"
            result += f"{ansiPrefix}{char}"
        
        # Join all parts into a single string
        return result
        #return '\n'.join(result)

    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
file_path = "C:\\Users\\Weaver\\Downloads\\example.txt"  # Replace with your file path
output = decode_ansi_file(file_path)
print(output)

with open("C:\\Users\\Weaver\\Downloads\\example_out.txt", "w") as file:
    file.write(output)

colorPrefix = ""
for i in range(0, 256):
    if i != 0: colorPrefix += " "
    colorPrefix += str(i)

print(colorPrefix)