import argostranslate.package
import argostranslate.translate
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3333"], allow_headers=["Content-Type"])


@app.route('/traducir', methods=['POST'])
def traducir():
    try:
        data = request.get_json()
        # Check if required fields are present in the request
        if 'in_code' not in data or 'out_code' not in data or 'text' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        in_code = data['in_code']
        out_code = data['out_code']
        text = data['text']

        # Perform translation logic (Replace this with your actual translation logic)
        translation = translate_text(text, in_code, out_code)

        response = {'translation': translation}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def translate_text(text, in_code, to_code):
    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    try:
        package_to_install = list(
            filter(
                lambda x: (x.from_code == in_code and x.to_code == to_code),
                available_packages,
            )
        )[0]
        argostranslate.package.install_from_path(package_to_install.download())
        tt = argostranslate.translate.translate(text, in_code, to_code)
    except IndexError as ie:
        return None
    return tt

if __name__ == '__main__':
    app.run(debug=True)
    # available_packages = argostranslate.package.get_available_packages()
    # print(*sorted(set([str(a).split(' ')[0] for a in available_packages])), sep='\n')
    # text = "The pretty girl has a bouquet of red flags"
    # x = from_to_text("en","zh",text)
    # print(x)