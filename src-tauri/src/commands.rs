use crate::types::{Service, Status};
use keyring::Keyring;

/// Save username/password for a gif service to the OS's keychain
#[tauri::command]
pub fn save_credentials(service: Service, username: String, password: String) -> Status {
  let service_name = service.to_keyring_name();
  let keyring = Keyring::new(&service_name, &username);

  match keyring.set_password(&password) {
    Ok(_) => Status::Success,
    Err(message) => Status::Failure(message.to_string()),
  }
}

/// Compress a video file with ffmpeg and return its path
fn compress_video(file_name: String) -> String {
	let output = std::process::Command::new("echo").arg("howdy").output().unwrap();
	println!("{:?}", std::str::from_utf8(&output.stdout));
	"".to_owned()
}

/// Upload video/gif to a service
#[tauri::command]
pub fn upload(service: Service, file_name: String, is_anonymous: bool) -> Status {
	let _video_file = compress_video(file_name);
	Status::Success
}
