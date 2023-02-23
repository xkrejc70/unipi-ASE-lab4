use actix_web::{get, web, App, HttpServer, Result, Responder};
use actix_web::web::Data;
use serde::Deserialize;
use serde::Serialize;
use edit_distance::edit_distance;

use reqwest;

#[derive(Deserialize)]
struct Params {
    a: String,
    b: String,
}

#[derive(Serialize)]
struct MyResult {
    res: String,
}

//update stats for service and op
fn update_stats(service: &str, op: &str) -> Result<(), reqwest::Error> {
    let url = format!("http://stats-service:5000/stats/{}/{}", service, op);
    let client = reqwest::blocking::Client::new();
    let _res = client.post(url)
        .send()?;
    Ok(())
}

#[get("/concat")]
async fn concat(path: web::Query<Params>) -> Result<impl Responder> {
    eprintln!("Got concat request");
    update_stats("str", "concat").expect("Failed to update stats");
    let result = MyResult {
        res: format!("{}{}", path.a, path.b),
    };
    Ok(web::Json(result))
}

#[get("/editdistance")]
async fn editdistance(path: web::Query<Params>) -> Result<impl Responder> {
    eprintln!("Got ed request");
    let ed = edit_distance(&path.a,&path.b);

    update_stats("str", "editdistance").expect("Failed to update stats");
    let result = MyResult {
        res: format!("{}", ed),
    };
    Ok(web::Json(result))
}

#[derive(Deserialize)]
struct Param {
    a: String,
}

#[get("/upper")]
async fn upper(path: web::Query<Param>) -> Result<impl Responder> {
    eprintln!("Got upper request");
    update_stats("str", "upper").expect("Failed to update stats");
    let result = MyResult {
        res: format!("{}", path.a.to_uppercase()),
    };
    Ok(web::Json(result))
}

#[get("/lower")]
async fn lower(path: web::Query<Param>) -> Result<impl Responder> {
    eprintln!("Got lower request");
    update_stats("str", "lower").expect("Failed to update stats");
    let result = MyResult {
        res: format!("{}", path.a.to_lowercase()),
    };
    Ok(web::Json(result))
}

pub fn init(config: &mut web::ServiceConfig) {
    config.service(
        web::scope("")
            .service(concat)
            .service(upper)
            .service(lower)
            .service(editdistance)
    );
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {   
    HttpServer::new(|| {
        App::new()
            .configure(init)
    })
    .bind("0.0.0.0:5000")?
    .run()
    .await
}