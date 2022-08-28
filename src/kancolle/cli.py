import click
import kancolle

@click.command()
def main():
    click.echo('か~ん~こ~れ!')
    print(kancolle.KanColle.quest('B185').code[0])


if __name__ == '__main__':
    main()
