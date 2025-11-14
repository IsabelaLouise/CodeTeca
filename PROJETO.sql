DROP DATABASE IF EXISTS CodeTeca;
CREATE DATABASE CodeTeca;
USE CodeTeca;

CREATE TABLE Usuario (
    ID_usuario INT PRIMARY KEY,
    Nome VARCHAR(50),
    Email VARCHAR(50),
    DtNasc DATE,
    Logradouro VARCHAR(50),
    Numero INT,
    CEP VARCHAR(50),
    Complemento VARCHAR(50)
);

CREATE TABLE Livro (
    ID_livro INT PRIMARY KEY,
    Titulo VARCHAR(50),
    Ano INT
);

CREATE TABLE Copia (
    ID_copia INT PRIMARY KEY,
    Estado VARCHAR(50),
    Disponibilidade VARCHAR(50),
    fk_Livro_ID_livro INT,
    FOREIGN KEY (fk_Livro_ID_livro)
        REFERENCES Livro(ID_livro)
        ON DELETE RESTRICT
);

CREATE TABLE Emprestimo_Empresta (
    ID_emprestimo INT PRIMARY KEY,
    DtEmprestimo DATE,
    DtDevolucao DATE,
    Status VARCHAR(50),
    DtDevolucaoPrevista DATE,
    fk_Usuario_ID_usuario INT,
    fk_Copia_ID_copia INT,
    FOREIGN KEY (fk_Usuario_ID_usuario)
        REFERENCES Usuario(ID_usuario),
    FOREIGN KEY (fk_Copia_ID_copia)
        REFERENCES Copia(ID_copia)
);

CREATE TABLE Multa (
    ID_multa INT PRIMARY KEY,
    Data DATE,
    Validade DATE,
    Motivo VARCHAR(50),
    fk_Emprestimo_Empresta_ID_emprestimo INT,
    FOREIGN KEY (fk_Emprestimo_Empresta_ID_emprestimo)
        REFERENCES Emprestimo_Empresta(ID_emprestimo)
        ON DELETE CASCADE
);

CREATE TABLE Autor (
    ID_autor INT PRIMARY KEY,
    NomeAutor VARCHAR(50),
    Nacionalidade VARCHAR(50),
    DtNascAutor DATE
);

CREATE TABLE Livro_Autor (
    ID_livro INT,
    ID_autor INT,
    PRIMARY KEY (ID_livro, ID_autor),
    FOREIGN KEY (ID_livro) REFERENCES Livro(ID_livro),
    FOREIGN KEY (ID_autor) REFERENCES Autor(ID_autor)
);

INSERT INTO Usuario 
(ID_usuario, Nome, Email, DtNasc, Logradouro, Numero, CEP, Complemento)
VALUES 
(1, 'Adair Silva', 'adair123@gmail.com', '1967-08-05', 'Rua Manoel Sanches', 67, '8876542', 'ap 200'),
(2, 'Isabela Louise', 'isabelalll@icloud.com', '2007-06-05', 'Rua Agua Verde', 18, '81220093', 'casa 4'),
(3, 'Fatima Maria', 'fatima1955@yahoo.com.br', '1955-03-13', 'Rua Machado de Assis', 344, '2344432', 'casa 9'),
(4, 'Rosana Lourdes', 'rosana345@yahoo.com', '1989-09-30', 'Rua Ostia de Jesus', 76, '1119879', 'ap 3'),
(5, 'Guilherme Pereira', 'guizinhogameplay@gmail.com', '2010-11-02', 'Rua Imaculada da Conceção', 1222, '1182987', 'predio 2'),
(6, 'Bernadete Oliveira', 'deteoliv@yahoo.com.br', '1954-04-02', 'Rua das Flores', 181, '81689450', 'casa 5'),
(7, 'Odete Machado', 'machado1968@yahoo.com.br', '1968-11-12', 'Rua Joaquim Rocha', 71, '82379250' , 'apto 35'),
(8, 'Enzo da Costa', 'enzonewgen@gmail.com', '2011-08-22', 'Rua Praia Bela', 1897, '90908765', 'casa 20'),
(9, 'Valentina Molina', 'moliboo@gmail.com', '2009-07-17', 'Rua Dom Pedro I', 1145, '88876652', 'apto 21'),
(10, 'Robert Cenci', 'cencirobert@yahoo.com.br', '1976-10-03', 'Rua Tiradentes', 31, '87834765', 'casa 28'),
(11, 'Mariana Lopes', 'marilopes@gmail.com', '1999-05-12', 'Avenida Brasil', 215, '81230540', 'Ap 302, Bloco B'),
(12, 'Felipe Andrade', 'felipe.andrade@hotmail.com', '1987-09-23', 'Rua das Flores', 88, '82340012', 'Fundos'),
(13, 'Ana Beatriz Souza', 'anabia.souza@gmail.com', '2001-03-14', 'Rua XV de Novembro', 1001, '80250000', 'Ap 1203'),
(14, 'Lucas Martins', 'lucasmartins@yahoo.com', '1995-01-27', 'Rua Pioneiro José da Silva', 56, '81470025', 'Casa 3'),
(15, 'Carolina Mendes', 'carolmendes@gmail.com', '1992-07-09', 'Rua das Palmeiras', 320, '81010350', 'Ap 402, Bloco A'),
(16, 'Gustavo Ramos', 'gustavo.ramos@hotmail.com', '1984-11-30', 'Avenida República', 45, '81150510', 'Casa 2'),
(17, 'Juliana Castro', 'julianacastro@gmail.com', '2000-12-18', 'Rua São João', 197, '81620480', 'Ap 101, Bloco C');
SELECT * FROM Usuario;

INSERT INTO Livro (ID_livro, Titulo, Ano)
VALUES (1, 'Dom Casmurro', 1899),
	(2, 'O Cortiço', 1890),
	(3, 'Memórias Póstumas de Brás Cubas', 1881),
	(4, 'Capitães da Areia', 1937),
	(5, 'Iracema', 1865),
	(6, 'Vidas Secas', 1938),
	(7, 'O Primo Basílio', 1878),
	(8, 'O Guarani', 1857),
	(9, 'A Moreninha', 1844),
	(10, 'Quincas Borba', 1891),
    (11, 'O Tribunal dos Mortos', 2025),
	(12, 'Minha Lady Jane', 2017),
	(13, 'Belas adormecidas', 2017),
	(14, 'Will e Will', 2013),
    (15, 'A Cidade e as Serras', 1901),
	(16, 'O Alienista', 1882),
	(17, 'Mar Morto', 1936);
    
SELECT * FROM Livro;

INSERT INTO Livro_Autor (ID_livro, ID_autor)
VALUES
(1, 1),  
(2, 2), 
(3, 1),  
(4, 3), 
(5, 4), 
(6, 5),  
(7, 6),  
(8, 4),  
(9, 7),  
(10, 1),
(11, 8),
(11, 9),
(12, 10),
(12, 11),
(12, 12),
(13, 13),
(13, 14),
(14, 15),
(14, 16),
(15, 6),
(16, 1),
(17, 3);
SELECT * FROM Livro_Autor;



INSERT INTO Copia (ID_copia, Estado, Disponibilidade, fk_Livro_ID_livro)
VALUES (1, 'Novo', 'Disponível', 1),
	(2, 'Bom', 'Indisponível', 2),
	(3, 'Regular', 'Disponível', 3),
	(4, 'Novo', 'Disponível', 4),
	(5, 'Bom', 'Disponível', 5),
	(6, 'Regular', 'Indisponível', 6),
	(7, 'Bom', 'Disponível', 7),
	(8, 'Novo', 'Disponível', 8),
	(9, 'Regular', 'Indisponível', 9),
	(10, 'Bom', 'Disponível', 10),
	(11, 'Novo', 'Disponível', 11),
	(12, 'Regular', 'Disponível', 11),
	(13, 'Bom', 'Indisponível', 11),
	(14, 'Novo', 'Disponível', 12),
	(15, 'Bom', 'Disponível', 12),
	(16, 'Regular', 'Indisponível', 12),
	(17, 'Novo', 'Disponível', 13),
	(18, 'Bom', 'Disponível', 13),
	(19, 'Regular', 'Disponível', 13),
	(20, 'Novo', 'Disponível', 14),
	(21, 'Bom', 'Indisponível', 14),
	(22, 'Regular', 'Disponível', 14),
	(23, 'Novo', 'Disponível', 1),
	(24, 'Bom', 'Disponível', 2),
	(25, 'Regular', 'Indisponível', 3),
	(26, 'Bom', 'Disponível', 4),
	(27, 'Novo', 'Disponível', 5);
SELECT * FROM Copia;

INSERT INTO Emprestimo_Empresta
(ID_emprestimo, DtEmprestimo, DtDevolucao, DtDevolucaoPrevista, Status, fk_Usuario_ID_usuario, fk_Copia_ID_copia)
VALUES (1, '2025-09-26', '2025-10-10', '2025-10-05', 'Em andamento', 1, 2),
	(2, '2025-09-20', '2025-09-30', '2025-09-29', 'Devolvido', 2, 6),
	(3, '2025-09-15', '2025-09-28', '2025-09-25', 'Em andamento', 3, 3),
	(4, '2025-09-10', '2025-09-25', '2025-09-23', 'Devolvido', 4, 1),
	(5, '2025-09-05', '2025-09-19', '2025-09-15', 'Atrasado', 5, 9),
	(6, '2025-09-02', '2025-09-16', '2025-09-13', 'Devolvido', 6, 5),
	(7, '2025-09-01', '2025-09-15', '2025-09-14', 'Em andamento', 7, 7),
	(8, '2025-08-30', '2025-09-13', '2025-09-10', 'Devolvido', 10, 4),
	(9, '2025-08-25', '2025-09-08', '2025-09-05', 'Atrasado', 9, 8),
	(10, '2025-08-20', '2025-09-03', '2025-09-01', 'Em andamento', 8, 10),
	(11, '2025-10-01', '2025-10-15', '2025-10-13', 'Devolvido', 3, 11),
	(12, '2025-10-05', NULL, '2025-12-18', 'Em andamento', 4, 12),
	(13, '2025-10-08', NULL,'2025-10-20', 'Atrasado', 5, 13),
	(14, '2025-10-10', '2025-10-24', '2025-10-22', 'Em andamento', 6, 14),
	(15, '2025-10-12', '2025-10-26', '2025-10-25', 'Devolvido', 7, 15),
	(16, '2025-10-14', '2025-10-28', '2025-10-27', 'Atrasado', 8, 16),
	(17, '2025-10-18', '2025-11-01', '2025-10-30', 'Devolvido', 9, 17),
	(18, '2025-10-20', '2025-11-03', '2025-11-02', 'Devolvido', 10, 18);
SELECT * FROM Emprestimo_Empresta;

INSERT INTO Multa (ID_multa, Data, Validade, Motivo, fk_Emprestimo_Empresta_ID_emprestimo)
VALUES (1, '2024-09-20', '2024-10-20', 'Atraso na devolução', 1), 
	(2, '2024-09-08', '2024-10-08', 'Livro danificado', 9), 
    (3, '2024-09-12', '2024-10-12', 'Extravio do exemplar', 3), 
    (4, '2024-09-18', '2024-10-18', 'Atraso na devolução', 2), 
    (5, '2024-09-26', '2024-10-26', 'Atraso na devolução', 1), 
    (6, '2024-09-16', '2024-10-16', 'Livro danificado', 6), 
    (7, '2024-09-15', '2024-10-15', 'Extravio do exemplar', 7), 
    (8, '2024-09-13', '2024-10-13', 'Atraso na devolução', 9), 
    (9, '2024-09-10', '2024-10-10', 'Livro danificado', 4), 
    (10, '2024-09-09', '2024-10-09', 'Extravio do exemplar', 10),
    (11, '2024-03-10', '2024-04-10', 'Atraso na devolução', 11),
	(12, '2024-04-15', '2024-05-15', 'Livro danificado', 12),
	(13, '2024-05-20', '2024-06-20', 'Extravio do exemplar', 13),
	(14, '2024-06-05', '2024-07-05', 'Atraso na devolução', 14),
	(15, '2024-07-10', '2024-08-10', 'Livro danificado', 15),
	(16, '2024-07-25', '2024-08-25', 'Extravio do exemplar', 16),
	(17, '2024-08-12', '2024-09-12', 'Atraso na devolução', 17),
	(18, '2024-09-18', '2024-10-18', 'Livro danificado', 18),
	(19, '2023-11-03', '2023-12-03', 'Extravio do exemplar', 4),
	(20, '2023-12-20', '2024-01-20', 'Atraso na devolução', 7);
SELECT * FROM Multa;

INSERT INTO Autor (ID_autor, NomeAutor, Nacionalidade, DtNascAutor)
VALUES(1, 'Machado de Assis', 'Brasil', '1839-06-21'),
	(2, 'Aluísio Azevedo', 'Brasil', '1857-04-14'),
    (3, 'Jorge Amado', 'Brasil', '1912-08-10'),
    (4, 'José de Alencar', 'Brasil', '1829-05-01'),
    (5, 'Graciliano Ramos', 'Brasil', '1892-10-27'),
    (6, 'Eça de Queirós', 'Portugal', '1845-11-25'),
    (7, 'Joaquim Manuel de Macedo', 'Brasil', '1820-06-24'),
    (8, 'Rick Riordan', 'Estados Unidos', '1964-06-05'),
    (9, 'Mark Oshiro', 'Estados Unidos', '1983-10-23'),
    (10, 'Cynthia Hand', 'Estados Unidos', '1978-12-14'),
    (11, 'Brodi Ashton', 'Estados Unidos', '1984-08-30'),
    (12, 'Jodi Meadows', 'Estados Unidos', '1983-05-02'),
    (13, 'Stephen King', 'Estados Unidos', '1947-09-21'),
    (14, 'Owen King', 'Estados Unidos', '1977-02-21'),
    (15, 'John Green', 'Estados Unidos', '1977-08-24'),
    (16, 'David Levithan', 'Estados Unidos', '1972-09-07');
SELECT * FROM Autor;    

UPDATE Livro SET fk_Autor_ID_autor = 1 WHERE ID_livro = 1;
UPDATE Livro SET fk_Autor_ID_autor = 2 WHERE ID_livro = 2;
UPDATE Livro SET fk_Autor_ID_autor = 1 WHERE ID_livro = 3;
UPDATE Livro SET fk_Autor_ID_autor = 3 WHERE ID_livro = 4;
UPDATE Livro SET fk_Autor_ID_autor = 4 WHERE ID_livro = 5;
UPDATE Livro SET fk_Autor_ID_autor = 5 WHERE ID_livro = 6;
UPDATE Livro SET fk_Autor_ID_autor = 6 WHERE ID_livro = 7;
UPDATE Livro SET fk_Autor_ID_autor = 4 WHERE ID_livro = 8;
UPDATE Livro SET fk_Autor_ID_autor = 7 WHERE ID_livro = 9;
UPDATE Livro SET fk_Autor_ID_autor = 1 WHERE ID_livro = 10;


SELECT Nome, Email
FROM Usuario
ORDER BY Nome;

SELECT Nome, DtNasc, TIMESTAMPDIFF(YEAR, DtNasc, CURDATE()) AS Idade
FROM Usuario
ORDER BY DtNasc DESC;

SELECT 
    Livro.Titulo AS 'Nome do Livro',
    COUNT(Copia.ID_copia) AS 'Quantidade de Cópias'
FROM Livro
LEFT JOIN Copia ON Copia.fk_Livro_ID_livro = Livro.ID_livro
GROUP BY Livro.Titulo
ORDER BY Livro.Titulo;

SELECT 
    SUM(Quantidade) AS 'Total de Cópias na Biblioteca'
FROM (
    SELECT COUNT(*) AS Quantidade
    FROM Copia
    GROUP BY fk_Livro_ID_livro
) AS Subconsulta;

SELECT 
    ROUND(AVG(TIMESTAMPDIFF(YEAR, DtNasc, CURDATE())), 1) AS 'Média de Idade dos Usuários'
FROM Usuario;

SELECT 
    L.ID_livro AS 'Código do Livro',
    L.Titulo AS 'Título',
    L.Ano AS 'Ano de Publicação',
    GROUP_CONCAT(A.NomeAutor SEPARATOR ', ') AS 'Autores'
FROM Livro L
JOIN Livro_Autor LA ON L.ID_livro = LA.ID_livro
JOIN Autor A ON LA.ID_autor = A.ID_autor
GROUP BY L.ID_livro, L.Titulo, L.Ano
ORDER BY L.ID_livro;

SELECT 
	Usuario.Nome AS 'Usuário',
    Livro.Titulo AS 'Livro Emprestado',
    Emprestimo_Empresta.DtEmprestimo AS 'Data do Empréstimo'
    FROM Usuario
    JOIN Emprestimo_Empresta ON Usuario.ID_usuario = Emprestimo_Empresta.fk_Usuario_ID_Usuario
    JOIN Copia ON Emprestimo_Empresta.fk_Copia_ID_copia = Copia.ID_copia
    JOIN Livro ON Copia.fk_Livro_ID_livro = Livro.ID_livro;

SELECT 
    Usuario.Nome AS 'Usuário',
    Livro.Titulo AS 'Livro',
    Emprestimo_Empresta.DtDevolucaoPrevista AS 'Data Prevista',
    Emprestimo_Empresta.DtDevolucao AS 'Data Devolução',
    Multa.Valor AS 'Valor da Multa'
FROM Usuario
JOIN Emprestimo_Empresta 
    ON Usuario.ID_usuario = Emprestimo_Empresta.fk_Usuario_ID_usuario
JOIN Copia 
    ON Emprestimo_Empresta.fk_Copia_ID_copia = Copia.ID_copia
JOIN Livro 
    ON Copia.fk_Livro_ID_livro = Livro.ID_livro
JOIN Multa 
    ON Emprestimo_Empresta.ID_emprestimo = Multa.fk_Emprestimo_ID_emprestimo;
    
SELECT 
    Usuario.Nome AS 'Usuário',
    Livro.Titulo AS 'Livro',
    Emprestimo_Empresta.DtEmprestimo AS 'Data do Empréstimo',
    Multa.Motivo AS 'Motivo da Multa'
FROM Usuario
JOIN Emprestimo_Empresta 
    ON Usuario.ID_usuario = Emprestimo_Empresta.fk_Usuario_ID_usuario
JOIN Copia 
    ON Emprestimo_Empresta.fk_Copia_ID_copia = Copia.ID_copia
JOIN Livro 
    ON Copia.fk_Livro_ID_livro = Livro.ID_livro
JOIN Multa 
    ON Emprestimo_Empresta.ID_emprestimo = Multa.fk_Emprestimo_Empresta_ID_emprestimo;

SELECT 
    Livro.Titulo AS 'Título do Livro',
    COUNT(Copia.ID_copia) AS 'Quantidade de Cópias',
    GROUP_CONCAT(DISTINCT Autor.NomeAutor SEPARATOR ', ') AS 'Autores'
FROM Livro
JOIN Copia 
    ON Livro.ID_livro = Copia.fk_Livro_ID_livro
JOIN Livro_Autor 
    ON Livro.ID_livro = Livro_Autor.ID_livro
JOIN Autor 
    ON Livro_Autor.ID_autor = Autor.ID_autor
GROUP BY Livro.Titulo
ORDER BY Livro.Titulo;

DELIMITER //
CREATE PROCEDURE ConsultarMultasPorUsuario(IN p_ID_usuario INT)
BEGIN
    SELECT 
        U.Nome AS 'Usuário',
        M.Motivo AS 'Motivo da Multa',
        M.Data AS 'Data da Multa',
        M.Validade AS 'Validade da Multa'
    FROM Usuario U
    JOIN Emprestimo_Empresta E 
        ON U.ID_usuario = E.fk_Usuario_ID_usuario
    JOIN Multa M 
        ON E.ID_emprestimo = M.fk_Emprestimo_Empresta_ID_emprestimo
    WHERE U.ID_usuario = p_ID_usuario;
END //
DELIMITER ;

CALL ConsultarMultasPorUsuario(5);

DROP TABLE IF EXISTS MultaLog;
CREATE TABLE MultaLog (
    ID_log INT AUTO_INCREMENT PRIMARY KEY,
    Operacao CHAR(6) NOT NULL,
    DataAlteracao DATETIME NOT NULL,
    UsuarioBD VARCHAR(50) NOT NULL,
    OldID_multa INT NULL,
    NewID_multa INT NULL,
    OldMotivo VARCHAR(50) NULL,
    NewMotivo VARCHAR(50) NULL,
    OldData DATE NULL,
    NewData DATE NULL,
    OldValidade DATE NULL,
    NewValidade DATE NULL,
    OldEmprestimo INT NULL,
    NewEmprestimo INT NULL
);

DELIMITER $$
CREATE TRIGGER MultaLog_Insert
AFTER INSERT ON Multa
FOR EACH ROW
BEGIN
    INSERT INTO MultaLog (Operacao, DataAlteracao, UsuarioBD,
        NewID_multa, NewMotivo, NewData, NewValidade, NewEmprestimo)
    VALUES ('INSERT', NOW(), CURRENT_USER(),
        NEW.ID_multa, NEW.Motivo, NEW.Data, NEW.Validade, NEW.fk_Emprestimo_Empresta_ID_emprestimo);
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER MultaLog_Update
AFTER UPDATE ON Multa
FOR EACH ROW
BEGIN
    INSERT INTO MultaLog (Operacao, DataAlteracao, UsuarioBD,
        OldID_multa, NewID_multa,
        OldMotivo, NewMotivo,
        OldData, NewData,
        OldValidade, NewValidade,
        OldEmprestimo, NewEmprestimo)
    VALUES ('UPDATE', NOW(), CURRENT_USER(),
        OLD.ID_multa, NEW.ID_multa,
        OLD.Motivo, NEW.Motivo,
        OLD.Data, NEW.Data,
        OLD.Validade, NEW.Validade,
        OLD.fk_Emprestimo_Empresta_ID_emprestimo, NEW.fk_Emprestimo_Empresta_ID_emprestimo);
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER MultaLog_Delete
AFTER DELETE ON Multa
FOR EACH ROW
BEGIN
    INSERT INTO MultaLog (Operacao, DataAlteracao, UsuarioBD,
        OldID_multa, OldMotivo, OldData, OldValidade, OldEmprestimo)
    VALUES ('DELETE', NOW(), CURRENT_USER(),
        OLD.ID_multa, OLD.Motivo, OLD.Data, OLD.Validade, OLD.fk_Emprestimo_Empresta_ID_emprestimo);
END$$
DELIMITER ;


INSERT INTO Multa (ID_multa, Data, Validade, Motivo, fk_Emprestimo_Empresta_ID_emprestimo)
VALUES (21, '2025-11-10', '2025-12-10', 'Extravio do exemplar', 3);

UPDATE Multa SET Motivo = 'Atraso na devolução' WHERE ID_multa = 21;

DELETE FROM Multa WHERE ID_multa = 21;

SELECT * FROM MultaLog;
