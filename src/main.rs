use sycamore::prelude::*;
use wasm_bindgen::prelude::wasm_bindgen;
//NOTE to self... there is bug in the Sycamore example.
// It would behoove you to create a pull request
// Deeply, for this project we can munge index.js to perform the API call
// Then, ingest user input here for the desired reactivity to WASM effect!
#[wasm_bindgen(module = "/js/index.js")]
extern "C" {
    fn multiply(a: f64, b: f64) -> f64;
}

#[component]
fn App<G: Html>(cx: Scope) -> View<G> {
    let a = create_signal(cx, "0");
    let b = create_signal(cx, "0");
    let product = create_signal(cx, 0_f64);

    create_effect(cx, || {
        product.set(multiply(
            *(a.get().parse::<f64>().unwrap()),
            *(a.get().parse::<f64>().unwrap()),
        ));
    });

    view! { cx,
        input(type="number", bind:value=a)
        span { "*" }
        input(type="number", bind:value=b)
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
