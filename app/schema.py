instructions = [
    'DROP TABLE IF EXISTS users;',
    'DROP TABLE IF EXISTS entries;',
    '''
    CREATE TABLE users (
      id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(50) NOT NULL,
      email VARCHAR(50) NOT NULL,
      password VARCHAR(255) NOT NULL,
      age INT NOT NULL
    );
    ''',
    '''
    CREATE TABLE entries (
      id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
      emotion VARCHAR(50) NOT NULL,
      description TEXT NOT NULL,
      created_by INT NOT NULL,
      created_at DATETIME NOT NULL,
      modified_at DATETIME NOT NULL,
      FOREIGN KEY (created_by) REFERENCES users(id)
    );
    '''
]




