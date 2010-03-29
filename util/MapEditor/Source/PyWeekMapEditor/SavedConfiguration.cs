using System;
using System.Windows;
using System.Windows.Controls;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace PyWeekMapEditor
{
	public class SavedConfiguration
	{
		private bool loaded = false;
		private string user = "";
		private static List<string> users = new List<string>(new string[] { "blake", "falun", "ikr", "kirin", "other", "ph1n", "spears" });
		private string rootFolder;

		private void Load()
		{
			if (System.IO.File.Exists("config.txt"))
			{
				try
				{
					string[] lines = System.IO.File.ReadAllText("config.txt").Split('\n');
					this.user = lines[0].Trim();
					this.rootFolder = lines[1].Trim();
					this.loaded = true;
					return;
				}
				catch (Exception) { }
			}
			InformationDialog d = new InformationDialog();
			d.ShowDialog();
			this.user = d.User;
			this.rootFolder = d.RootPath;
			this.loaded = true;
			this.Save();
		}

		private void Save()
		{
			string output = this.user + "\n" + this.RootPath;

			System.IO.File.WriteAllText("config.txt", output);
		}

		public string User
		{
			get
			{
				if (!this.loaded)
				{
					this.Load();
				}
				return this.user;
			}
		}

		public string RootPath
		{
			get
			{
				if (!this.loaded)
				{
					this.Load();
				}
				return this.rootFolder;
			}
		}

		public string Prefix
		{
			get
			{
				return this.User[0] + "";
			}
		}

		private class InformationDialog : System.Windows.Window
		{
			public InformationDialog()
			{
				this.Width = 300;
				this.Height = 200;
				ComboBox cb = new ComboBox() { ItemsSource = SavedConfiguration.users };
				cb.Padding = new Thickness(8);
				cb.SelectionChanged += new SelectionChangedEventHandler(cb_SelectionChanged);
				StackPanel sp = new StackPanel();
				this.Content = sp;
				sp.Children.Add(new TextBlock() { Text = "Who are you?" });
				sp.Children.Add(cb);
				Button b = new Button() { Content = "OK", Padding = new Thickness(8) };
				b.Click += new RoutedEventHandler(b_Click);
				sp.Children.Add(b);
			}

			void cb_SelectionChanged(object sender, SelectionChangedEventArgs e)
			{
				this.User = ((ComboBox)sender).SelectedItem.ToString();
			}

			void b_Click(object sender, RoutedEventArgs e)
			{
				this.Close();
				System.Windows.MessageBox.Show("Pick the root folder of your PyWeek enlistment. The one containing /tiles/ and /levels/...");
				System.Windows.Forms.FolderBrowserDialog folderDialog = new System.Windows.Forms.FolderBrowserDialog();
				folderDialog.ShowDialog();
				this.RootPath = folderDialog.SelectedPath;
			}

			public string RootPath { get; set; }
			public string User { get; set; }
		}
	}
}
