import os
import random
import string
import subprocess
from moviepy.editor import *

# Fungsi untuk mendapatkan nama acak untuk file hasil
def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Meminta input nama file video yang ingin diolah
input_video_filename = input("Masukkan nama file video input: ")

# Memeriksa apakah file video input ada dan berada di direktori yang sama dengan skrip
if not os.path.isfile(input_video_filename):
    print("File video input tidak ditemukan.")
else:
    # Membuat direktori "hasil" jika belum ada
    output_folder = "hasil"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Baca video dengan resolusi rendah
    video_low_res = VideoFileClip(input_video_filename)

    # Interpolasi resolusi video rendah menjadi 720x1280
    video_low_res_interpolated = video_low_res.resize((720, 1280))

    # Simpan video rendah resolusi yang telah diinterpolasi sebagai file sementara
    output_video_temp_resized_filename = os.path.join(output_folder, random_string(8) + "_low_res_interpolated.mp4")
    video_low_res_interpolated.write_videofile(output_video_temp_resized_filename, codec='libx264')

    # Mengubah resolusi video tinggi menjadi 720x1280 agar sesuai dengan video rendah yang telah diinterpolasi
    video_high_res = VideoFileClip(input_video_filename).resize((720, 1280))

    # Simpan video tinggi resolusi yang telah diubah resolusinya sebagai file sementara
    output_video_temp_high_res_filename = os.path.join(output_folder, random_string(8) + "_high_res.mp4")
    video_high_res.write_videofile(output_video_temp_high_res_filename, codec='libx264')

    # Gabungkan video rendah resolusi yang telah diinterpolasi dan video tinggi resolusi menggunakan FFmpeg
    output_final_filename = os.path.join(output_folder, random_string(8) + "_final.mp4")
    ffmpeg_cmd = f'ffmpeg -i {output_video_temp_resized_filename} -i {output_video_temp_high_res_filename} -filter_complex "[0:v]fps=30,setpts=PTS-STARTPTS[low_res];[1:v]fps=30,setpts=PTS-STARTPTS[high_res];[low_res][1:a][high_res][1:a]concat=n=2:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" -y {output_final_filename}'
    subprocess.call(ffmpeg_cmd, shell=True)

    # Hapus file sementara video rendah resolusi yang telah diinterpolasi dan video tinggi resolusi
    os.remove(output_video_temp_resized_filename)
    os.remove(output_video_temp_high_res_filename)

    print(f"Video hasil disimpan di folder 'hasil' dengan nama file {os.path.basename(output_final_filename)}.")
