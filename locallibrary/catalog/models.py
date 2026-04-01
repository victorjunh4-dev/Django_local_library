from django.db import models
from django.urls import reverse  # Usado em get_absolute_url() para obter o URL de um ID específico
from django.db.models import UniqueConstraint  # Restringe campos a valores únicos
from django.db.models.functions import Lower  # Retorna o valor do campo em letras minúsculas
from django.contrib.auth.models import User  # Importando o modelo User para o campo borrower
import uuid

class Genre(models.Model):
    """Modelo que representa um gênero de livro."""
    name = models.CharField(
        max_length=200,
        unique=True,  # Verifica se o valor do atributo é único
        help_text="Digite um gênero de livro (ex: Ficção Científica, Poesia Francesa etc.)"
    )

    def __str__(self):
        """Retorna uma representação do objeto do modelo."""
        return self.name

    def get_absolute_url(self):
        """Retorna o URL para acessar uma instância específica de gênero."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),  # Transforma o nome para minúsculas
                name='genre_name_case_insensitive_unique',
                violation_error_message="Gênero já existe (comparação insensível a maiúsculas/minúsculas)"
            ),
        ]

class Language(models.Model):
    """Modelo que representa o idioma de um livro"""
    name = models.CharField(
        max_length=20,
        unique=True,
    )

    def __str__(self):
        """Retorna uma representação do objeto do modelo."""
        return self.name

    def get_absolute_url(self):
        """Retorna o URL para acessar uma instância específica de idioma."""
        return reverse('language-detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                Lower('name'),  # Transforma o nome para minúsculas
                name='language_name_case_insensitive_unique',
                violation_error_message="Idioma já existe (comparação insensível a maiúsculas/minúsculas)"
            ),
        ]

class Author(models.Model):
    """Modelo que representa um autor de livro"""
    name = models.CharField(
        max_length=50,
        unique=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    date_of_death = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                Lower('name'),  # Transforma o nome para minúsculas
                name='author_name_case_insensitive_unique',
                violation_error_message="Nome já existe (comparação insensível a maiúsculas/minúsculas)"
            ),
        ]

class Book(models.Model):
    """Modelo que representa um livro"""
    title = models.CharField(
        max_length=50,
        help_text="Digite o título do livro (ex: O Senhor dos Anéis)"
    )

    author = models.ForeignKey(
        'Author',
        on_delete=models.RESTRICT,
        null=True
    )

    summary = models.TextField(
        max_length=150,
        help_text="Digite um resumo do livro"
    )

    isbn = models.CharField(
        'ISBN', max_length=13,
        unique=True,
        help_text='Número ISBN de 13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>'
    )

    genre = models.ManyToManyField(
        'Genre'
    )

    language = models.ForeignKey(
        'Language',
        on_delete=models.RESTRICT
    )

    def __str__(self):
        """Retorna uma representação do objeto do modelo."""
        return f'{self.title} por {self.author}'

    def get_absolute_url(self):
        """Retorna o URL para acessar o registro de detalhes deste livro."""
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        ordering = ['title']
        constraints = [
            UniqueConstraint(
                Lower('title'),  # Transforma o título para minúsculas
                name='book_title_case_insensitive_unique',
                violation_error_message="Livro já existe (comparação insensível a maiúsculas/minúsculas)"
            ),
        ]

class BookInstance(models.Model):
    """Modelo que representa uma instância de um livro"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para esta instância específica de livro em toda a biblioteca"
    )
    
    due_back = models.DateField(
        null=True,
        blank=True
    )

    LOAN_STATUS = (
        ('m', 'Manutenção'),
        ('o', 'Emprestado'),
        ('a', 'Disponível'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro',
    )

    book = models.ForeignKey(
        'Book',
        verbose_name="Livro",
        on_delete=models.RESTRICT
    )

    imprint = models.CharField(
        max_length=255,  # Aumentei o tamanho do campo para acomodar mais informações sobre a editora
        help_text="Informações sobre a editora ou impressão"
    )

    borrower = models.ForeignKey(
        User,  # Certifique-se de importar o modelo User corretamente
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """Retorna uma representação do objeto do modelo."""
        return f'{self.id} ({self.book.title})'
    
    def get_absolute_url(self):
        """Retorna o URL para acessar o registro de detalhes desta instância de livro."""
        return reverse('bookinstance-detail', args=[str(self.id)])