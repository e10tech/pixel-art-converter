import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import io


def create_pixel_art(image, pixel_size=10):
    # ピクセルアート化（ドット絵化）関数
    original_width, original_height = image.size
    new_width = max(1, original_width // pixel_size)
    new_height = max(1, original_height // pixel_size)
    small_image = image.resize((new_width, new_height), Image.NEAREST)
    pixel_art = small_image.resize((original_width, original_height), Image.NEAREST)
    return pixel_art


def quantize_to_16bit(image: Image.Image) -> Image.Image:
    # 16ビット（RGB565）風に減色
    arr = np.array(image)
    arr[..., 0] = (arr[..., 0] >> 3) << 3  # R
    arr[..., 1] = (arr[..., 1] >> 2) << 2  # G
    arr[..., 2] = (arr[..., 2] >> 3) << 3  # B
    return Image.fromarray(arr, "RGB")


def to_grayscale(image: Image.Image) -> Image.Image:
    # モノクロ（グレースケール）変換
    return image.convert("L").convert("RGB")


def to_colorful(image: Image.Image, factor=2.0) -> Image.Image:
    # 彩度アップでカラフルに（factorは大きいほど派手！）
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def apply_palette_style(image: Image.Image, style: str) -> Image.Image:
    # カラースタイルに応じて変換
    if style == "16ビット風":
        return quantize_to_16bit(image)
    elif style == "モノクロ":
        return to_grayscale(image)
    elif style == "カラフル":
        return to_colorful(image)
    else:
        return image  # デフォルトはそのまま


def main():
    st.title("🎮 ピクセルアート・ビフォーアフター比較メーカー")
    st.write(
        "オリジナル画像と変換後ピクセルアートを横並びで見比べできるよ！カラースタイルも選べる😊"
    )

    uploaded_file = st.file_uploader(
        "画像を選んでね",
        type=["png", "jpg", "jpeg", "gif", "bmp"],
        help="PNG, JPG, JPEG, GIF, BMP形式が使えるよ",
    )

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
        except Exception as e:
            st.error("画像の読み込みでエラーが出ちゃった…😢 ファイルを確認してみてね！")
            return

        if image.mode != "RGB":
            image = image.convert("RGB")

        # カラースタイル選択！
        style = st.selectbox(
            "カラースタイルを選ぼう！",
            ["16ビット風", "モノクロ", "カラフル"],
            help="好きな雰囲気でピクセルアートを楽しめるよ",
        )

        # ピクセルサイズ調整
        pixel_size = st.slider(
            "ピクセルサイズ（大きいほどドット感UP！）",
            min_value=2,
            max_value=50,
            value=10,
            step=1,
            help="小さいと細かいドット絵、大きいとカクカク感が強くなるよ",
        )

        # ピクセルアート＋カラースタイル変換
        with st.spinner("ピクセルアートを作成中…"):
            pixel_art = create_pixel_art(image, pixel_size)
            styled_art = apply_palette_style(pixel_art, style)

        # 横並びでビフォーアフター比較！
        col1, col2 = st.columns(2)
        # タイトルの高さを揃えるため、2行に分けて明示的に<br>で改行
        with col1:
            st.markdown("### 🖼️ オリジナル画像<br>&nbsp;", unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        with col2:
            st.markdown(f"### 🎨 ピクセルアート<br>（{style}）", unsafe_allow_html=True)
            st.image(styled_art, use_container_width=True)

        # ダウンロードボタン
        buf = io.BytesIO()
        styled_art.save(buf, format="PNG")
        buf.seek(0)
        st.download_button(
            label=f"{style}ピクセルアートをダウンロード",
            data=buf,
            file_name=f"{style}_pixel_art_{pixel_size}.png",
            mime="image/png",
        )

        # 画像情報
        with st.expander("📝 画像情報"):
            st.write(f"**元のサイズ**: {image.size[0]} × {image.size[1]} pixels")
            st.write(f"**ピクセルサイズ**: {pixel_size}")
            st.write(
                f"**ダウンサンプルサイズ**: {max(1, image.size[0] // pixel_size)} × {max(1, image.size[1] // pixel_size)} pixels"
            )


if __name__ == "__main__":
    main()
# 250629_GeminiCLI/main_new.py
