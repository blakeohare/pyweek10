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
	/// Interaction logic for VictoryXDialog.xaml
	/// </summary>
	public partial class VictoryXDialog : Window
	{
		private string originalValue;
		private string finalValue;
		private bool saved = false;

		public VictoryXDialog(string originalValue)
		{
			this.originalValue = originalValue;
			InitializeComponent();
			if (string.IsNullOrEmpty(originalValue))
			{
				originalValue = "0";
			}
			this.xInput.Text = originalValue;
			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
		}

		void CancelButton_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void SaveButton_Click(object sender, RoutedEventArgs e)
		{
			this.saved = true;
			this.finalValue = this.xInput.Text;
			this.Close();
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
	}
}
