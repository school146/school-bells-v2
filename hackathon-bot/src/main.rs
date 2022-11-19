use teloxide::prelude::*;

[tokio::main]
async fn main() {
    println!("Bot started");

    let bot = Bot::new();
    println!("{:?}", bot);
}
