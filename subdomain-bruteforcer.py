import sys


if len(sys.argv) < 3:
    print("Usage: python script_name.py organization_name wordlist")
    sys.exit(1)

base_domain = sys.argv[1]
words_file_path =  sys.argv[2]
def generate_fake_domains(word_list, base_domain):
    fake_domains = [f"{word}.{base_domain}" for word in word_list]
    return fake_domains

def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write('\n'.join(data))

if __name__ == "__main__":
    
    output_file_path = base_domain+"_fake_subdomains.txt"

    # Read the list of words from the file
    with open(words_file_path, 'r') as file:
        word_list = [line.strip() for line in file]

    # Generate fake domains
    fake_domains = generate_fake_domains(word_list, base_domain)

    # Write the fake domains to the output file
    write_to_file(output_file_path, fake_domains)
