import subprocess

def run_llama_model(input_text):
    # Path to the Ollama executable
    ollama_path = "C:\\Users\\ayham\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
    
    # Command to run the LLaMa model
    command = [ollama_path, "run", "llama3.2"]

    try:
        # Running the command and capturing output
        result = subprocess.run(command, input=input_text, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running Ollama:")
        print(e.stderr)
    except FileNotFoundError:
        print("Ollama executable not found. Please check the path:", ollama_path)
    except Exception as e:
        print("An unexpected error occurred:", str(e))

# Test the function with sample input
run_llama_model("Who created you?")
