from merge import merge
from split import split, save_image


def main():
    image_path = "./tests/images/test.jpg"
    window_size = (300, 400)
    use_percent = False
    x_shift = 250
    y_shift = 300
    split_dir = "./split_res/"
    merge_dir = "./merge_res/"

    result_dir = split(image_path, window_size, use_percent, x_shift, y_shift, split_dir)

    image_merged = merge(result_dir)

    save_image(image_merged, merge_dir, "merged.jpg")


if __name__ == '__main__':
    main()
