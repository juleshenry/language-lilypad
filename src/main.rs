use sycamore::prelude::*;
use wasm_bindgen::prelude::wasm_bindgen;
//NOTE to self... there is bug in the Sycamore example.
// It would behoove you to create a pull request
// Deeply, for this project we can munge index.js to perform the API call
// Then, ingest user input here for the desired reactivity to WASM effect!
#[wasm_bindgen(module = "/js/index.js")]
extern "C" {
    fn multiply(a: String) -> String;
}

#[component]
fn App<G: Html>(cx: Scope) -> View<G> {
    let a = create_signal(cx, String::new());
    // // let b = create_signal(cx, String::from("0").as_str());
    let product = create_signal(cx, String::new());

    create_effect(cx, || {
        product.set(multiply(a.get().to_string()));
    });

    view! { cx,
        input(type="text", bind:value=a)
        span { "times" }
        // input(type="number", bind:value=b)
        span { "=" }
        span { (*product.get()) }
    }
}

fn main() {
    sycamore::render(|cx| {
        view! { cx,
            App
        }
    });
}