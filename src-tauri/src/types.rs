use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub enum Status {
  Success,
  Failure(String),
}

#[derive(Serialize, Deserialize)]
pub enum Service {
  Gfycat,
  Streamable,
}

impl Service {
  pub fn to_keyring_name(&self) -> String {
    let service_name = serde_json::to_string(&self)
      .unwrap_or(String::from(""))
      .replace("\"", "")
      .to_lowercase();
		
		String::from("shadow_cat") + "_" + &service_name
  }
}
