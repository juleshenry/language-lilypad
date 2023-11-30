import argostranslate.package
import argostranslate.translate
from flask import Flask, request, jsonify


def from_to_text(from_code, to_code, text):
    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    try:
        # FROM 2 TO
        package_to_install = list(
            filter(
                lambda x: (x.from_code == from_code and x.to_code == to_code),
                available_packages,
            )
        )[0]
        argostranslate.package.install_from_path(package_to_install.download())
        # Translate
        tt = argostranslate.translate.translate(text, from_code, to_code)
    except IndexError as ie:
        return None
    return tt

app = Flask(__name__)

@app.route('/traducir', methods=['POST'])
def traducir():
    try:
        data = request.get_json()

        # Check if required fields are present in the request
        if 'from_code' not in data or 'out_code' not in data or 'text' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        from_code = data['from_code']
        out_code = data['out_code']
        text = data['text']

        # Perform translation logic (Replace this with your actual translation logic)
        translation = translate_text(text, from_code, out_code)

        response = {'translation': translation}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def translate_text(text, from_code, out_code):
    # Replace this function with your actual translation logic
    # For simplicity, this example returns the input text as is
    return from_to_text(from_code, out_code, text)

if __name__ == '__main__':
    app.run(debug=True)
    # available_packages = argostranslate.package.get_available_packages()
    # print(*sorted(set([str(a).split(' ')[0] for a in available_packages])), sep='\n')
    # text = "The pretty girl has a bouquet of red flags"
    # x = from_to_text("en","zh",text)
    # print(x)