import click


@click.command()
@click.argument("user-name")
def main(user_name):
    print(f"Hello click {user_name}")


if __name__ == "__main__":
    main()