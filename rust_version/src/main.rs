use sycamore::prelude::*;
use wasm_bindgen::prelude::wasm_bindgen;
// use wasm_bindgen::JsValue;
// use std::future::Future;

#[wasm_bindgen(module = "/js/index.js")]
extern "C" {
    fn fetch_def(a: String) -> String;
}


// fn convert_future_to_string(fut: String) -> String {
//     return String::from("Hello, world!");
// }

#[component]
fn App<G: Html>(cx: Scope) -> View<G> {
    let a = create_signal(cx, String::new());
    let product = create_signal(cx, String::new());

    create_effect(cx, || {
        let user_input = a.get().to_string();
        product.set(fetch_def(user_input));
    });

    view! { cx,
        input(type="text", bind:value=a)
        div { (*product.get()) }
    }
}

fn main() {
    sycamore::render(|cx| {
        view! { cx,
            App
        }
    });
}
