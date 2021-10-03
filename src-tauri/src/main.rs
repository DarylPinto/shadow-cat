#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

mod commands;
mod types;

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
      commands::save_credentials,
      commands::upload
    ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
