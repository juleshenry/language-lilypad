use tikv_client_ffi::{TranslateRequest, TranslateResponse};

fn main() {
    let translate_request = TranslateRequest {
        source_language: "en",
        target_language: "fr",
        text: "Hello, world!",
    };

    let translate_response = tikv_client_ffi::translate(&translate_request);

    match translate_response {
        Ok(response) => {
            println!("Translation: {}", response.translated_text);
        }
        Err(error) => {
            eprintln!("Translation error: {:?}", error);
        }
    }
}

