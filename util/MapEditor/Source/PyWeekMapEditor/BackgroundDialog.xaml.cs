using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace PyWeekMapEditor
{
	/// <summary>
	/// Interaction logic for BackgroundDialog.xaml
	/// </summary>
	public partial class BackgroundDialog : Window
	{
		public BackgroundDialog(string image_file, string scroll_rate)
		{
			InitializeComponent();
			this.file = image_file;
			this.FilenameDisplay.Text = "Currently selected: " + (string.IsNullOrEmpty(image_file) ? "(none)" : image_file);
			this.scroll_rate.Text = scroll_rate;
			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
			this.ChooseButton.Click += new RoutedEventHandler(ChooseButton_Click);
			this.ClearButton.Click += new RoutedEventHandler(ClearButton_Click);
		}

		void ClearButton_Click(object sender, RoutedEventArgs e)
		{
			this.file = "";
			this.FilenameDisplay.Text = "Currently selected: (none)";
		}

		private string file = "";
		public string File { get { return this.file; } }

		public string ScrollRate { get { return this.scroll_rate.Text; } }

		void ChooseButton_Click(object sender, RoutedEventArgs e)
		{
			System.Windows.Forms.OpenFileDialog dialog = new System.Windows.Forms.OpenFileDialog();
			dialog.InitialDirectory = MainWindow.BackgroundsDirectory;
			
			dialog.ShowDialog();
			string filename = dialog.FileName;
			if (!string.IsNullOrEmpty(filename))
			{
				file = filename;
				file = System.IO.Path.GetFileNameWithoutExtension(file);
				this.FilenameDisplay.Text = "Currently selected: " + file;
			}
		}

		void CancelButton_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void SaveButton_Click(object sender, RoutedEventArgs e)
		{
			this.Saved = true;
			this.Close();
		}
		public bool Saved { get; set; }
	}

}
