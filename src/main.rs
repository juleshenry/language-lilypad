// main.rs

use sycamore::prelude::*;

fn main() {
    sycamore::render(|cx| view! { cx,
        p { 
            span { "Hello, World!" }
        }
    });
}
