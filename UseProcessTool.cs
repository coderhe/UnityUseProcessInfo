using UnityEditor;
using System.Diagnostics;

public class UseProcessTool : Editor
{
    [MenuItem("Tools/调用Bat脚本")]
    public static void RunBatScript( )
    {
        Process pro = new Process();
         // 替换为你的 Bat 脚本路径
        pro.StartInfo.FileName = "C:\\Users\\Administrator\\Desktop\\Test.bat";
        pro.StartInfo.Arguments = " ";
        pro.StartInfo.UseShellExecute = false;
        pro.StartInfo.RedirectStandardOutput = true;
        pro.StartInfo.RedirectStandardInput = true;
        pro.StartInfo.CreateNoWindow = true;
        pro.Start();
        
        string output = pro.StandardOutput.ReadToEnd();
        pro.WaitForExit();
        pro.Close();
        UnityEngine.Debug.LogError(" output is " + output);
    }
	
	[MenuItem("Tools/调用Python脚本")]
    public static void RunPythonScript()
    {
        try
        {
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                WorkingDirectory = $"{XXXSVNRoot}/PythonWorkspace/Scripts",
                // 替换为你的 Python 解释器路径，如果已在环境变量中，可以直接使用 "python"
                FileName = "C:/Python27/python.exe",
                // 替换为你的 Python 脚本路径
                Arguments = $" {XXXSVNRoot}/PythonWorkspace/Scripts/UETools/UnityCallMethon.py", 
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
            };

            using (Process process = new Process { StartInfo = startInfo })
            {
                process.Start();
                // 读取 Python 脚本的输出
                string output = process.StandardOutput.ReadToEnd();
                // 读取 Python 脚本的错误输出
                string errorOutput = process.StandardError.ReadToEnd();
                process.WaitForExit();

                Debug.Log("Python Log： " + output);		
                // 处理错误输出
                if (!string.IsNullOrEmpty(errorOutput))
                {
                    Debug.LogError("Python Script Error: " + errorOutput);
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError("Error running Python script: " + e.Message);
        }
    }
}