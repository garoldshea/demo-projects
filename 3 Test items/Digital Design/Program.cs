using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace WordFrequency
{
    class Program
    {
        static void Main(string[] args)
        {
            // Проверяем, что переданы аргументы командной строки
            if (args.Length == 0)
            {
                Console.WriteLine("Пример использования: word_frequncy <filename>");
                return;
            }

            // Получаем имя файла из аргументов командной строки
            string filename = args[0];

            // Проверяем, что файл существует
            if (!File.Exists(filename))
            {
                Console.WriteLine("Файл не найден: {0}", filename);
                return;
            }

            // Читаем текст из файла и разбиваем его на слова
            string text = File.ReadAllText(filename);
            string[] words = Regex.Split(text, @"\W+");

            // Создаём словарь для хранения частотности слов
            Dictionary<string, int> wordFrequencies = new Dictionary<string, int>();

            // Проходимся по всем словам и увеличиваем счётчик для каждого слова
            foreach (string word in words)
            {
                string lowercaseWord = word.ToLower();
                if (wordFrequencies.ContainsKey(lowercaseWord))
                {
                    wordFrequencies[lowercaseWord]++;
                }
                else
                {
                    wordFrequencies[lowercaseWord] = 1;
                }
            }

            // Открытие файла для записи
            string filePath = "output.txt";
            StreamWriter writer = new StreamWriter(filePath);

            var sortedWords = from pair in wordFrequencies
                              orderby pair.Value descending
                              select pair;
            
            // Сортируем слова по убыванию частотности и записываем в файл               
            foreach (var pair in sortedWords)
            {
                writer.WriteLine("{0}: {1}", pair.Key, pair.Value);
            }

            // Закрытие файла
            writer.Close();

            Console.WriteLine("Результаты записаны в файл {0}", filePath);
            Console.ReadLine();
        }
    }
}