import sys

def generate_fake_domains(word_list, domains):
    fake_domains = [f"{word}.{domain}" for domain in domains for word in word_list]
    return fake_domains

def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write('\n'.join(data))

if __name__ == "__main__":
    domains_file =  sys.argv[1]
    words_file_path =  sys.argv[2]
    # Read the list of domains from the file
    with open(domains_file, 'r') as domain_file:
        domains = [line.strip() for line in domain_file]

    # Read the list of words from the file
    with open(words_file_path, 'r') as wordlist_file:
        word_list = [line.strip() for line in wordlist_file]

    # Generate fake domains for each domain in the list
    all_fake_domains = generate_fake_domains(word_list, domains)

    print(all_fake_domains)
