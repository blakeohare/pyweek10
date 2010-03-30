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
	/// Interaction logic for DefaultLocationDialog.xaml
	/// </summary>
	public partial class DefaultLocationDialog : Window
	{
		private string originalValue;
		private string finalValue;
		private bool saved = false;
		
		public DefaultLocationDialog(string originalValue, string locations)
		{
			this.originalValue = originalValue;

			InitializeComponent();
			List<string> choices = this.GetChoices(locations);
			this.choices.ItemsSource = choices;
			int index = choices.IndexOf(originalValue);
			if (index >= 0)
			{
				this.choices.SelectedIndex = index;
			}
			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
		}

		private List<string> GetChoices(string locations)
		{
			List<string> foo = new List<string>();
			if (!string.IsNullOrEmpty(locations))
			{
				foreach (string bar in locations.Split(' '))
				{
					string[] baz = bar.Split(',');
					foo.Add(baz[0]);
				}
			}
			return foo;
		}

		public string FinalValue
		{
			get
			{
				if (this.saved)
				{
					return this.finalValue;
				}
				return this.originalValue;
			}
		}

		void CancelButton_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void SaveButton_Click(object sender, RoutedEventArgs e)
		{
			this.saved = true;
			this.finalValue = this.choices.SelectedItem.ToString();
			this.Close();
		}
	}
}
