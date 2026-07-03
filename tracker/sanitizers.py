def strip_all_strings(data, fields=None):
    '''
    Clean whitespace from specific fields,
    or all string fields if no list is provided.
    '''
    if fields is None:
        fields = [
            key for key, value in data.items() if isinstance(value, str)
        ]

    for field in fields:
        value = data.get(field)
        if isinstance(value, str):
            data[field] = value.strip()

    return data

def clean_website_url(url):
    '''
    Standardizes URL input by stripping whitespace,
    and ensuring lowercase and a protocol prefix.
    '''
    if url:
        url = url.lower().strip()
        if not url.startswith(('http://', 'https://')):
            return f'https://{url}'
    # if the url is None or an empty string, it doesn't strip it
    # avoid getting an error
    return url

def upper_country_code(country_code):
    '''
    Ensure the country code is uppercase if it is a valid string.
    '''
    if isinstance(country_code, str):
        return country_code.upper()
    return country_code
