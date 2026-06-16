import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watermark or detect watermark in an image")
    parser.add_argument("mode", type=str, choices=["watermark", "detect"], help="Choose between watermark or detect functions")
    parser.add_argument("--message", type=str, help="String message to embed, end is cut if it's too long. UTF-8 encoding")
    parser.add_argument("--key", type=int, help="Key used for the transformation in the watermarking process")
    parser.add_argument( "--input_file", type=str, required=True, help="Path to the input image file")
    parser.add_argument("--output_file",type=str,required=False, default="./watermarked_image.png", help="Output file. Always used in watermark mode, only used in detect mode if it's a .txt file")
    args = parser.parse_args()

    if args.mode == "watermark":
        from algorithm.api import hide

        hide(args.message, args.key, args.input_file, args.output_file)
    elif args.mode == "detect":
        from algorithm.api import detect

        detected = detect(str, args.key, args.input_file)
        if args.output_file.endswith(".txt"):
            with open(args.output_file, "w") as f:
                f.write(str(detected))
        else:
            print(detected)